from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    # Core identifiers
    lecla_id = Column(String, primary_key=True)
    jnid = Column(String, unique=True, index=True)
    number = Column(String)  # Job number (e.g., #4356)
    name = Column(String)
    
    # Core info
    type = Column(String)  # Job type (e.g., "Roofing")
    service_type = Column(String)  # Service type (e.g., "Replacement")
    status_name = Column(String)  # Status (e.g., "Paid & Closed")
    
    # Contacts
    contact_id = Column(String, ForeignKey("contacts.lecla_id"))
    sales_rep = Column(String)  # Sales rep name
    primary_contact = Column(String)  # Primary contact name
    subcontractors = Column(JSON)  # Array of subcontractor names
    
    # Financial fields (from JobNimbus custom fields)
    total = Column(Float)  # Legacy field
    total_project = Column(Float)  # Total project cost
    total_gross = Column(Float)  # Gross revenue
    total_net = Column(Float)  # Net revenue (after fees)
    permit_fee = Column(Float)  # Permit costs
    financing_fee = Column(Float)  # Financing/credit card fees
    
    # Date fields (stored as Unix timestamps)
    first_estimate_signed_date = Column(Integer)  # When first estimate was signed
    second_estimate_signed_date = Column(Integer)  # Change order/re-sign date
    paid_in_full_date = Column(Integer)  # Final payment received
    file_date = Column(Integer)  # Job file creation/start date
    
    # Boolean/Logic fields
    is_repeat_customer = Column(Integer, default=0)  # SQLite boolean (0/1)
    warranty_and_permit_closed = Column(Integer, default=0)  # Job fully closed
    
    # System fields
    date_created = Column(Integer)
    date_updated = Column(Integer)
    data = Column(JSON)  # Full JobNimbus JSON for reference
    
    contact = relationship("Contact", back_populates="jobs")

class Contact(Base):
    __tablename__ = "contacts"
    
    lecla_id = Column(String, primary_key=True)
    jn_contact_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    date_created = Column(Integer)
    date_updated = Column(Integer)
    data = Column(JSON)
    
    jobs = relationship("Job", back_populates="contact")
    leads = relationship("Lead", back_populates="contact")

class Lead(Base):
    __tablename__ = "leads"
    
    lecla_id = Column(String, primary_key=True)
    contact_id = Column(String, ForeignKey("contacts.lecla_id"))
    source = Column(String)
    status = Column(String)
    notes = Column(Text)
    date_created = Column(Integer)
    date_updated = Column(Integer)
    
    contact = relationship("Contact", back_populates="leads")

class Budget(Base):
    __tablename__ = "budgets"
    
    jnid = Column(String, primary_key=True)
    number = Column(String)
    revenue = Column(Float)
    related_job_id = Column(String)
    sales_rep = Column(String)
    date_updated = Column(Integer)
    data = Column(JSON)

class Estimate(Base):
    __tablename__ = "estimates"
    
    jnid = Column(String, primary_key=True)
    number = Column(String)
    total = Column(Float)
    related_job_id = Column(String)
    status_name = Column(String)
    date_updated = Column(Integer)
    data = Column(JSON)

class Invoice(Base):
    __tablename__ = "invoices"
    
    jnid = Column(String, primary_key=True)
    number = Column(String)
    total = Column(Float)
    fees = Column(Float)
    related_job_id = Column(String)
    status_name = Column(String)
    date_created = Column(Integer)
    date_updated = Column(Integer)
    data = Column(Text)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    role = Column(String, default="sales")
    date_created = Column(Integer)

class Task(Base):
    """To-do items with assignments and due dates"""
    __tablename__ = "tasks"
    
    lecla_id = Column(String, primary_key=True)
    jnid = Column(String, unique=True, nullable=True)  # JobNimbus ID if synced
    title = Column(String, nullable=False)
    description = Column(Text)
    related_to_type = Column(String)  # "job", "contact", "lead"
    related_to_id = Column(String)  # FK to related entity
    assigned_to = Column(String, ForeignKey("users.id"))
    due_date = Column(Integer)  # Unix timestamp
    priority = Column(String, default="medium")  # "low", "medium", "high", "urgent"
    status = Column(String, default="pending")  # "pending", "in_progress", "completed", "cancelled"
    completed_at = Column(Integer)
    date_created = Column(Integer)
    date_updated = Column(Integer)
    data = Column(JSON)  # Additional metadata

class Workflow(Base):
    """Custom workflow templates (e.g., 'Residential Roof', 'Commercial Siding')"""
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    entity_type = Column(String)  # "job", "contact", "lead"
    is_active = Column(Integer, default=1)  # SQLite uses INTEGER for boolean
    display_order = Column(Integer)
    date_created = Column(Integer)

class WorkflowStatus(Base):
    """Statuses within a workflow (e.g., 'Lead', 'Quoted', 'Sold')"""
    __tablename__ = "workflow_statuses"
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey("workflows.id"))
    name = Column(String, nullable=False)
    color = Column(String)  # Hex color for UI
    display_order = Column(Integer)
    is_closed = Column(Integer, default=0)  # Terminal status
    
    workflow = relationship("Workflow")

class CustomField(Base):
    """User-defined custom fields with automation capabilities"""
    __tablename__ = "custom_fields"
    
    id = Column(String, primary_key=True)
    entity_type = Column(String)  # "job", "contact", "estimate", "invoice"
    field_name = Column(String, nullable=False)  # "First Estimate Signed Date"
    jn_field_key = Column(String)  # "first_estimate_signed_date" - JN API key
    field_type = Column(String)  # "date", "text", "number", "currency", "calculated"
    
    # Automation settings
    auto_populate = Column(Integer, default=0)  # Auto-fill this field
    auto_populate_trigger = Column(String)  # "status_change", "estimate_signed", "invoice_created"
    auto_populate_formula = Column(Text)  # Python expression or SQL
    
    # Calculated field settings
    is_calculated = Column(Integer, default=0)
    calculation_formula = Column(Text)  # e.g., "total - permit_fee - financing_fee"
    depends_on_fields = Column(JSON)  # List of field IDs this depends on
    
    # Display settings
    display_in_details = Column(Integer, default=1)
    display_in_timeline = Column(Integer, default=0)
    display_in_reports = Column(Integer, default=0)
    display_in_kanban = Column(Integer, default=0)
    display_order = Column(Integer)
    is_active = Column(Integer, default=1)
    
    date_created = Column(Integer)
    date_updated = Column(Integer)

class FieldValue(Base):
    """Stores actual custom field values for entities"""
    __tablename__ = "field_values"
    
    id = Column(String, primary_key=True)
    custom_field_id = Column(String, ForeignKey("custom_fields.id"))
    entity_type = Column(String)
    entity_id = Column(String)
    value = Column(Text)  # JSON for complex values
    date_updated = Column(Integer)
    updated_by = Column(String, ForeignKey("users.id"))
    
    custom_field = relationship("CustomField")
