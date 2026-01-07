from fastapi import APIRouter, HTTPException, Depends
from backend.app.database import get_db
from backend.app.models import Workflow, WorkflowStatus
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

router = APIRouter()

# Pydantic models
class WorkflowStatusCreate(BaseModel):
    name: str
    color: Optional[str] = "#3b82f6"
    display_order: int
    is_closed: bool = False

class WorkflowStatusResponse(BaseModel):
    id: str
    workflow_id: str
    name: str
    color: str
    display_order: int
    is_closed: int
    
    model_config = {"from_attributes": True}

class WorkflowCreate(BaseModel):
    name: str
    entity_type: str  # "job", "contact", "lead"
    statuses: List[WorkflowStatusCreate] = []

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class WorkflowResponse(BaseModel):
    id: str
    name: str
    entity_type: str
    is_active: int
    display_order: Optional[int]
    date_created: int
    statuses: List[WorkflowStatusResponse] = []
    
    model_config = {"from_attributes": True}

# Workflow endpoints
@router.get("/workflows", response_model=List[WorkflowResponse])
def get_workflows(
    entity_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all workflows with optional filtering"""
    query = db.query(Workflow)
    
    if entity_type:
        query = query.filter(Workflow.entity_type == entity_type)
    if is_active is not None:
        query = query.filter(Workflow.is_active == (1 if is_active else 0))
    
    workflows = query.order_by(Workflow.display_order.asc()).all()
    
    # Load statuses for each workflow
    for workflow in workflows:
        workflow.statuses = db.query(WorkflowStatus).filter(
            WorkflowStatus.workflow_id == workflow.id
        ).order_by(WorkflowStatus.display_order.asc()).all()
    
    return workflows

@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: str, db: Session =Depends(get_db)):
    """Get a single workflow by ID"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow.statuses = db.query(WorkflowStatus).filter(
        WorkflowStatus.workflow_id == workflow_id
    ).order_by(WorkflowStatus.display_order.asc()).all()
    
    return workflow

@router.post("/workflows", response_model=WorkflowResponse)
def create_workflow(workflow_data: WorkflowCreate, db: Session = Depends(get_db)):
    """Create a new workflow with statuses"""
    now = int(datetime.now().timestamp())
    
    workflow = Workflow(
        id=f"WF-{uuid.uuid4().hex[:8].upper()}",
        name=workflow_data.name,
        entity_type=workflow_data.entity_type,
        is_active=1,
        display_order=0,
        date_created=now
    )
    
    db.add(workflow)
    db.flush()  # Get workflow ID before adding statuses
    
    # Create statuses
    statuses = []
    for status_data in workflow_data.statuses:
        status = WorkflowStatus(
            id=f"WS-{uuid.uuid4().hex[:8].upper()}",
            workflow_id=workflow.id,
            name=status_data.name,
            color=status_data.color,
            display_order=status_data.display_order,
            is_closed=1 if status_data.is_closed else 0
        )
        db.add(status)
        statuses.append(status)
    
    db.commit()
    db.refresh(workflow)
    workflow.statuses = statuses
    
    return workflow

@router.put("/workflows/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(workflow_id: str, workflow_data: WorkflowUpdate, db: Session = Depends(get_db)):
    """Update a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow_data.name is not None:
        workflow.name = workflow_data.name
    if workflow_data.is_active is not None:
        workflow.is_active = 1 if workflow_data.is_active else 0
    if workflow_data.display_order is not None:
        workflow.display_order = workflow_data.display_order
    
    db.commit()
    db.refresh(workflow)
    
    workflow.statuses = db.query(WorkflowStatus).filter(
        WorkflowStatus.workflow_id == workflow_id
    ).order_by(WorkflowStatus.display_order.asc()).all()
    
    return workflow

@router.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """Delete a workflow and its statuses"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Delete associated statuses
    db.query(WorkflowStatus).filter(WorkflowStatus.workflow_id == workflow_id).delete()
    db.delete(workflow)
    db.commit()
    
    return {"status": "deleted", "workflow_id": workflow_id}

# Status endpoints
@router.post("/workflows/{workflow_id}/statuses", response_model=WorkflowStatusResponse)
def create_status(workflow_id: str, status_data: WorkflowStatusCreate, db: Session = Depends(get_db)):
    """Add a new status to a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    status = WorkflowStatus(
        id=f"WS-{uuid.uuid4().hex[:8].upper()}",
        workflow_id=workflow_id,
        name=status_data.name,
        color=status_data.color,
        display_order=status_data.display_order,
        is_closed=1 if status_data.is_closed else 0
    )
    
    db.add(status)
    db.commit()
    db.refresh(status)
    
    return status

@router.put("/statuses/{status_id}", response_model=WorkflowStatusResponse)
def update_status(status_id: str, status_data: WorkflowStatusCreate, db: Session = Depends(get_db)):
    """Update a status"""
    status = db.query(WorkflowStatus).filter(WorkflowStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    
    status.name = status_data.name
    status.color = status_data.color
    status.display_order = status_data.display_order
    status.is_closed = 1 if status_data.is_closed else 0
    
    db.commit()
    db.refresh(status)
    
    return status

@router.delete("/statuses/{status_id}")
def delete_status(status_id: str, db: Session = Depends(get_db)):
    """Delete a status"""
    status = db.query(WorkflowStatus).filter(WorkflowStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    
    db.delete(status)
    db.commit()
    
    return {"status": "deleted", "status_id": status_id}
