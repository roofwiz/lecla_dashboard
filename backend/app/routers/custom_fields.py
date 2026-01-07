from fastapi import APIRouter, HTTPException, Depends
from backend.app.database import get_db
from backend.app.models import CustomField, FieldValue, Invoice, Job
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
import uuid
import json

router = APIRouter()

# Pydantic models
class CustomFieldCreate(BaseModel):
    entity_type: str
    field_name: str
    jn_field_key: Optional[str] = None
    field_type: str
    auto_populate: bool = False
    auto_populate_trigger: Optional[str] = None
    is_calculated: bool = False
    calculation_formula: Optional[str] = None
    depends_on_fields: Optional[List[str]] = []
    display_in_details: bool = True
    display_in_timeline: bool = False
    display_in_reports: bool = False
    display_in_kanban: bool = False

class CustomFieldResponse(BaseModel):
    id: str
    entity_type: str
    field_name: str
    jn_field_key: Optional[str]
    field_type: str
    auto_populate: int
    auto_populate_trigger: Optional[str]
    is_calculated: int
    calculation_formula: Optional[str]
    display_in_details: int
    display_in_timeline: int
    display_in_reports: int
    display_in_kanban: int
    is_active: int
    
    model_config = {"from_attributes": True}

# Custom Field Definition Endpoints
@router.get("/custom-fields", response_model=List[CustomFieldResponse])
def get_custom_fields(
    entity_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all custom field definitions"""
    query = db.query(CustomField)
    
    if entity_type:
        query = query.filter(CustomField.entity_type == entity_type)
    if is_active is not None:
        query = query.filter(CustomField.is_active == (1 if is_active else 0))
    
    return query.order_by(CustomField.display_order.asc()).all()

@router.post("/custom-fields", response_model=CustomFieldResponse)
def create_custom_field(field_data: CustomFieldCreate, db: Session = Depends(get_db)):
    """Create a new custom field definition"""
    now = int(datetime.now().timestamp())
    
    field = CustomField(
        id=f"CF-{uuid.uuid4().hex[:8].upper()}",
        entity_type=field_data.entity_type,
        field_name=field_data.field_name,
        jn_field_key=field_data.jn_field_key,
        field_type=field_data.field_type,
        auto_populate=1 if field_data.auto_populate else 0,
        auto_populate_trigger=field_data.auto_populate_trigger,
        is_calculated=1 if field_data.is_calculated else 0,
        calculation_formula=field_data.calculation_formula,
        depends_on_fields=json.dumps(field_data.depends_on_fields) if field_data.depends_on_fields else None,
        display_in_details=1 if field_data.display_in_details else 0,
        display_in_timeline=1 if field_data.display_in_timeline else 0,
        display_in_reports=1 if field_data.display_in_reports else 0,
        display_in_kanban=1 if field_data.display_in_kanban else 0,
        display_order=0,
        is_active=1,
        date_created=now,
        date_updated=now
    )
    
    db.add(field)
    db.commit()
    db.refresh(field)
    
    return field

# Field Value Endpoints
@router.get("/fields/{entity_type}/{entity_id}")
def get_entity_field_values(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    """Get all custom field values for an entity"""
    
    # Get field definitions
    fields = db.query(CustomField).filter(
        CustomField.entity_type == entity_type,
        CustomField.is_active == 1
    ).all()
    
    # Get stored values
    values = db.query(FieldValue).filter(
        FieldValue.entity_type == entity_type,
        FieldValue.entity_id == entity_id
    ).all()
    
    value_map = {v.custom_field_id: v.value for v in values}
    
    # Calculate calculated fields
    result = {}
    for field in fields:
        if field.is_calculated:
            # Calculate value based on formula
            calculated_value = calculate_field_value(field, entity_type, entity_id, value_map, db)
            result[field.id] = {
                "field_id": field.id,
                "field_name": field.field_name,
                "field_type": field.field_type,
                "value": calculated_value,
                "is_calculated": True
            }
        else:
            result[field.id] = {
                "field_id": field.id,
                "field_name": field.field_name,
                "field_type": field.field_type,
                "value": value_map.get(field.id),
                "is_calculated": False
            }
    
    return result

@router.put("/fields/{entity_type}/{entity_id}/{field_id}")
def update_field_value(
    entity_type: str,
    entity_id: str,
    field_id: str,
    value: Any,
    db: Session = Depends(get_db)
):
    """Update a custom field value"""
    field = db.query(CustomField).filter(CustomField.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    
    if field.is_calculated:
        raise HTTPException(status_code=400, detail="Cannot manually update calculated field")
    
    # Find or create field value
    field_value = db.query(FieldValue).filter(
        FieldValue.custom_field_id == field_id,
        FieldValue.entity_type == entity_type,
        FieldValue.entity_id == entity_id
    ).first()
    
    now = int(datetime.now().timestamp())
    
    if field_value:
        field_value.value = str(value)
        field_value.date_updated = now
    else:
        field_value = FieldValue(
            id=f"FV-{uuid.uuid4().hex[:8].upper()}",
            custom_field_id=field_id,
            entity_type=entity_type,
            entity_id=entity_id,
            value=str(value),
            date_updated=now
        )
        db.add(field_value)
    
    db.commit()
    
    # Trigger recalculation of dependent fields
    recalculate_dependent_fields(field_id, entity_type, entity_id, db)
    
    return {"status": "updated", "value": value}

# Auto-population trigger
@router.post("/auto-populate/{entity_type}/{entity_id}")
def trigger_auto_population(
    entity_type: str,
    entity_id: str,
    trigger_event: str,  # "status_change", "estimate_signed", etc.
    db: Session = Depends(get_db)
):
    """Trigger auto-population for fields based on an event"""
    
    # Find fields that should auto-populate for this trigger
    fields = db.query(CustomField).filter(
        CustomField.entity_type == entity_type,
        CustomField.auto_populate == 1,
        CustomField.auto_populate_trigger == trigger_event,
        CustomField.is_active == 1
    ).all()
    
    now = int(datetime.now().timestamp())
    updated_fields = []
    
    for field in fields:
        # Auto-populate based on trigger
        value = None
        
        if trigger_event == "estimate_signed" and field.field_type == "date":
            # Auto-fill with current timestamp
            value = now
        elif trigger_event == "invoice_created" and field.field_type == "date":
            value = now
        
        if value is not None:
            # Store the value
            field_value = db.query(FieldValue).filter(
                FieldValue.custom_field_id == field.id,
                FieldValue.entity_type == entity_type,
                FieldValue.entity_id == entity_id
            ).first()
            
            if field_value:
                field_value.value = str(value)
                field_value.date_updated = now
            else:
                field_value = FieldValue(
                    id=f"FV-{uuid.uuid4().hex[:8].upper()}",
                    custom_field_id=field.id,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    value=str(value),
                    date_updated=now
                )
                db.add(field_value)
            
            updated_fields.append(field.field_name)
    
    db.commit()
    
    return {"status": "auto-populated", "fields_updated": updated_fields}

# Helper functions
def calculate_field_value(field: CustomField, entity_type: str, entity_id: str, value_map: dict, db: Session):
    """Calculate a field's value based on its formula"""
    
    if not field.calculation_formula:
        return None
    
    formula = field.calculation_formula
    
    # Special handling for invoice net calculation
    # Formula: "total - permit_fee - financing_fee"
    if entity_type == "invoice" and field.field_type == "currency":
        # Get the invoice
        invoice = db.query(Invoice).filter(Invoice.jnid == entity_id).first()
        if not invoice:
            return None
        
        total = invoice.total or 0
        
        # Get permit fee and financing fee from custom fields
        permit_fee = 0
        financing_fee = 0
        
        for field_id, value in value_map.items():
            custom_field = db.query(CustomField).filter(CustomField.id == field_id).first()
            if custom_field and custom_field.jn_field_key == "permit_fee":
                try:
                    permit_fee = float(value) if value else 0
                except:
                    permit_fee = 0
            elif custom_field and custom_field.jn_field_key == "financing_fee":
                try:
                    financing_fee = float(value) if value else 0
                except:
                    financing_fee = 0
        
        # Calculate net amount
        net_amount = total - permit_fee - financing_fee
        return net_amount
    
    return None

def recalculate_dependent_fields(changed_field_id: str, entity_type: str, entity_id: str, db: Session):
    """Recalculate any fields that depend on this field"""
    
    # Find fields that depend on the changed field
    all_fields = db.query(CustomField).filter(
        CustomField.entity_type == entity_type,
        CustomField.is_calculated == 1
    ).all()
    
    for field in all_fields:
        if field.depends_on_fields:
            depends_on = json.loads(field.depends_on_fields) if isinstance(field.depends_on_fields, str) else field.depends_on_fields
            if changed_field_id in depends_on:
                # Recalculate this field
                values = db.query(FieldValue).filter(
                    FieldValue.entity_type == entity_type,
                    FieldValue.entity_id == entity_id
                ).all()
                value_map = {v.custom_field_id: v.value for v in values}
                
                new_value = calculate_field_value(field, entity_type, entity_id, value_map, db)
                
                # Store calculated value (for caching)
                field_value = db.query(FieldValue).filter(
                    FieldValue.custom_field_id == field.id,
                    FieldValue.entity_type == entity_type,
                    FieldValue.entity_id == entity_id
                ).first()
                
                now = int(datetime.now().timestamp())
                
                if field_value:
                    field_value.value = str(new_value) if new_value is not None else None
                    field_value.date_updated = now
                else:
                    field_value = FieldValue(
                        id=f"FV-{uuid.uuid4().hex[:8].upper()}",
                        custom_field_id=field.id,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        value=str(new_value) if new_value is not None else None,
                        date_updated=now
                    )
                    db.add(field_value)
                
                db.commit()
