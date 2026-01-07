from fastapi import APIRouter, HTTPException, Depends
from backend.app.database import get_db
from backend.app.models import Task
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

router = APIRouter()

# Pydantic models for validation
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    related_to_type: Optional[str] = None  # "job", "contact", "lead"
    related_to_id: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[int] = None
    priority: str = "medium"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    lecla_id: str
    jnid: Optional[str]
    title: str
    description: Optional[str]
    related_to_type: Optional[str]
    related_to_id: Optional[str]
    assigned_to: Optional[str]
    due_date: Optional[int]
    priority: str
    status: str
    completed_at: Optional[int]
    date_created: int
    date_updated: int
    
    model_config = {"from_attributes": True}

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    related_to_type: Optional[str] = None,
    related_to_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get tasks with optional filtering"""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if related_to_type:
        query = query.filter(Task.related_to_type == related_to_type)
    if related_to_id:
        query = query.filter(Task.related_to_id == related_to_id)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    
    return query.order_by(Task.due_date.asc()).all()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    """Get a single task by ID"""
    task = db.query(Task).filter(Task.lecla_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    now = int(datetime.now().timestamp())
    
    task = Task(
        lecla_id=f"T-{uuid.uuid4().hex[:8].upper()}",
        title=task_data.title,
        description=task_data.description,
        related_to_type=task_data.related_to_type,
        related_to_id=task_data.related_to_id,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
        priority=task_data.priority,
        status="pending",
        date_created=now,
        date_updated=now
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task"""
    task = db.query(Task).filter(Task.lecla_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.assigned_to is not None:
        task.assigned_to = task_data.assigned_to
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.status is not None:
        task.status = task_data.status
        if task_data.status == "completed":
            task.completed_at = int(datetime.now().timestamp())
    
    task.date_updated = int(datetime.now().timestamp())
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(Task).filter(Task.lecla_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"status": "deleted", "task_id": task_id}
