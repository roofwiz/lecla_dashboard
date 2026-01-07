import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'backend' / 'lecla.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Adding new columns to jobs table...")

new_columns = [
    ("service_type", "TEXT"),
    ("sales_rep", "TEXT"),
    ("primary_contact", "TEXT"),
    ("subcontractors", "JSON"),
    ("total_project", "REAL"),
    ("total_gross", "REAL"),
    ("total_net", "REAL"),
    ("permit_fee", "REAL"),
    ("financing_fee", "REAL"),
    ("first_estimate_signed_date", "INTEGER"),
    ("second_estimate_signed_date", "INTEGER"),
    ("paid_in_full_date", "INTEGER"),
    ("file_date", "INTEGER"),
    ("is_repeat_customer", "INTEGER DEFAULT 0"),
    ("warranty_and_permit_closed", "INTEGER DEFAULT 0"),
]

for col_name, col_type in new_columns:
    try:
        cursor.execute(f"ALTER TABLE jobs ADD COLUMN {col_name} {col_type}")
        print(f"✓ Added column: {col_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"  Column {col_name} already exists")
        else:
            print(f"✗ Error adding {col_name}: {e}")

conn.commit()
conn.close()

print("\n✓ Migration complete!")
