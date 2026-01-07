import sqlite3
import json
import os
from contextlib import contextmanager

DB_PATH = "backend/lecla.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Jobs Table (Lecla CRM)
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        jnid TEXT UNIQUE,
        lecla_id TEXT PRIMARY KEY,
        number TEXT,
        name TEXT,
        type TEXT,
        status_name TEXT,
        total REAL,
        contact_id TEXT,
        date_created INTEGER,
        date_updated INTEGER,
        data JSON,
        FOREIGN KEY(contact_id) REFERENCES contacts(lecla_id)
    )''')
    
    # Contacts Table
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        lecla_id TEXT PRIMARY KEY,
        jn_contact_id TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip TEXT,
        date_created INTEGER,
        date_updated INTEGER,
        data JSON
    )''')

    # Leads Table
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        lecla_id TEXT PRIMARY KEY,
        contact_id TEXT,
        source TEXT,
        status TEXT,
        notes TEXT,
        date_created INTEGER,
        date_updated INTEGER,
        FOREIGN KEY(contact_id) REFERENCES contacts(lecla_id)
    )''')
    
    # Budgets Table
    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
        jnid TEXT PRIMARY KEY,
        number TEXT,
        revenue REAL,
        related_job_id TEXT,
        sales_rep TEXT,
        date_updated INTEGER,
        data JSON
    )''')
    
    # Estimates Table
    c.execute('''CREATE TABLE IF NOT EXISTS estimates (
        jnid TEXT PRIMARY KEY,
        number TEXT,
        total REAL,
        related_job_id TEXT,
        status_name TEXT,
        date_updated INTEGER,
        data JSON
    )''')

    # Invoices table
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        jnid TEXT PRIMARY KEY,
        number TEXT,
        total REAL,
        fees REAL,
        related_job_id TEXT,
        status_name TEXT,
        date_created INTEGER,
        date_Updated INTEGER,
        data TEXT
    )''')

    # Users Table for Auth
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password_hash TEXT,
        full_name TEXT,
        role TEXT DEFAULT 'sales',
        date_created INTEGER
    )''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
