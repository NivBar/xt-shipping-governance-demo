"""
Database initialization script for XT Shipping Management System
GOVERNANCE ISSUE: No database backup strategy
GOVERNANCE ISSUE: No encryption at rest
"""

import sqlite3
import os
from datetime import datetime, timedelta

# SECURITY ISSUE: Hardcoded database path
DB_PATH = 'xt_shipping.db'

def init_database():
    """Initialize the database with schema and seed data"""
    
    # GOVERNANCE ISSUE: No connection pooling, no connection limits
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    print("✓ Database schema created")
    
    # Seed sample data
    seed_vessels(cursor)
    seed_cargo(cursor)
    seed_crew(cursor)
    seed_financial_transactions(cursor)
    seed_maintenance_records(cursor)
    seed_compliance_records(cursor)
    
    conn.commit()
    conn.close()
    
    print("✓ Database initialized successfully")
    print(f"✓ Database file: {DB_PATH}")
    print("\n⚠️  WARNING: This database contains intentional governance and security issues!")
    print("⚠️  For educational/demonstration purposes only!\n")

def seed_vessels(cursor):
    """Seed vessel data - GOVERNANCE ISSUE: Some vessels have expired certifications"""
    vessels = [
        ('XT Horizon', 'IMO9876543', 'Container Ship', 'Panama', 50000, 2015, 'Active', 
         '2025-01-15', '2026-07-15', '2025-12-31'),  # GOVERNANCE ISSUE: Insurance expires soon
        ('XT Navigator', 'IMO9876544', 'Bulk Carrier', 'Liberia', 75000, 2018, 'Active',
         '2024-06-20', '2025-06-20', '2024-03-15'),  # GOVERNANCE ISSUE: Insurance EXPIRED
        ('XT Pioneer', 'IMO9876545', 'Tanker', 'Marshall Islands', 100000, 2020, 'Active',
         '2025-03-10', '2026-03-10', '2026-08-30'),
        ('XT Explorer', 'IMO9876546', 'Container Ship', 'Singapore', 45000, 2012, 'Maintenance',
         '2023-11-05', '2024-11-05', '2025-05-20'),  # GOVERNANCE ISSUE: Inspection OVERDUE
        ('XT Voyager', 'IMO9876547', 'Ro-Ro Vessel', 'Cyprus', 30000, 2019, 'Active',
         '2025-02-28', '2026-02-28', '2026-01-15'),
    ]
    
    cursor.executemany('''
        INSERT INTO vessels (vessel_name, imo_number, vessel_type, flag_state, gross_tonnage, 
                           year_built, status, last_inspection_date, next_inspection_due, insurance_expiry)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', vessels)
    
    print("✓ Seeded 5 vessels (with governance issues)")

def seed_cargo(cursor):
    """Seed cargo data - GOVERNANCE ISSUE: Dangerous goods not properly tracked"""
    today = datetime.now().date()
    cargo_data = [
        (1, 'Electronics', 'Consumer electronics - laptops, phones', 500.5, 'Shanghai', 'Rotterdam', 
         today - timedelta(days=10), today + timedelta(days=5), 'In Transit', 0, 1, 3, 3),
        # GOVERNANCE ISSUE: Same person (user 3) created and approved
        (2, 'Grain', 'Wheat grain for export', 15000.0, 'New Orleans', 'Lagos',
         today - timedelta(days=5), today + timedelta(days=20), 'In Transit', 0, 0, 3, 3),
        (1, 'Chemicals', 'Industrial chemicals - Class 8 Corrosive', 200.0, 'Hamburg', 'Singapore',
         today - timedelta(days=3), today + timedelta(days=12), 'In Transit', 1, 1, 2, 2),
        # GOVERNANCE ISSUE: Dangerous goods, same person created and approved
        (3, 'Crude Oil', 'Crude petroleum', 50000.0, 'Saudi Arabia', 'Japan',
         today - timedelta(days=15), today + timedelta(days=10), 'In Transit', 1, 1, 2, 3),
        # GOVERNANCE ISSUE: Dangerous goods approved by different person but no dual authorization
        (4, 'Automobiles', 'New vehicles for export', 800.0, 'Detroit', 'Dubai',
         today - timedelta(days=20), today - timedelta(days=2), 'Delivered', 0, 1, 3, 2),
    ]
    
    cursor.executemany('''
        INSERT INTO cargo (vessel_id, cargo_type, description, weight_tons, origin_port, 
                          destination_port, loading_date, estimated_arrival, status, 
                          dangerous_goods, customs_cleared, created_by, approved_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', cargo_data)
    
    print("✓ Seeded 5 cargo records (with SoD violations)")

def seed_crew(cursor):
    """Seed crew data - GOVERNANCE ISSUE: Expired certificates, excessive hours"""
    today = datetime.now().date()
    crew_data = [
        ('Captain James Wilson', 'Master', 1, 'UK', 'GB123456', 'CERT-001', 
         today + timedelta(days=180), today - timedelta(days=365), today + timedelta(days=365), 220, 'Active'),
        # GOVERNANCE ISSUE: 220 hours worked (legal limit typically 180-200)
        ('Chief Engineer Maria Santos', 'Chief Engineer', 1, 'Philippines', 'PH789012', 'CERT-002',
         today - timedelta(days=30), today - timedelta(days=730), today + timedelta(days=365), 195, 'Active'),
        # GOVERNANCE ISSUE: Certificate EXPIRED 30 days ago
        ('First Officer Ahmed Hassan', 'First Officer', 2, 'Egypt', 'EG345678', 'CERT-003',
         today + timedelta(days=90), today - timedelta(days=180), today + timedelta(days=365), 185, 'Active'),
        ('Second Engineer Li Wei', 'Second Engineer', 2, 'China', 'CN901234', 'CERT-004',
         today + timedelta(days=365), today - timedelta(days=90), today + timedelta(days=365), 240, 'Active'),
        # GOVERNANCE ISSUE: 240 hours - SEVERE violation of working hours
        ('Bosun Carlos Rodriguez', 'Bosun', 3, 'Spain', 'ES567890', 'CERT-005',
         today + timedelta(days=200), today - timedelta(days=200), today + timedelta(days=365), 175, 'Active'),
        ('AB Seaman John Smith', 'Able Seaman', 1, 'USA', 'US234567', 'CERT-006',
         today - timedelta(days=10), today - timedelta(days=100), today + timedelta(days=365), 160, 'Active'),
        # GOVERNANCE ISSUE: Certificate expired 10 days ago
    ]
    
    cursor.executemany('''
        INSERT INTO crew (full_name, position, vessel_id, nationality, passport_number, 
                         certificate_number, certificate_expiry, contract_start, contract_end, 
                         hours_worked_this_month, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', crew_data)
    
    print("✓ Seeded 6 crew members (with compliance violations)")

def seed_financial_transactions(cursor):
    """Seed financial data - GOVERNANCE ISSUE: Same person creates and approves"""
    today = datetime.now().date()
    transactions = [
        ('Fuel Purchase', 1, 125000.00, 'USD', 'Bunker fuel - Rotterdam', 'INV-2025-001', 4, 4, 'Paid', today - timedelta(days=15)),
        # GOVERNANCE ISSUE: Same person (user 4) created and approved $125k transaction
        ('Port Fees', 2, 15000.00, 'USD', 'Port charges - Lagos', 'INV-2025-002', 3, 4, 'Paid', today - timedelta(days=10)),
        ('Maintenance', 4, 85000.00, 'USD', 'Engine overhaul', 'INV-2025-003', 2, 2, 'Pending', today - timedelta(days=5)),
        # GOVERNANCE ISSUE: Same person approved $85k maintenance
        ('Crew Wages', 1, 45000.00, 'USD', 'Monthly crew salaries', 'INV-2025-004', 4, 4, 'Paid', today - timedelta(days=3)),
        ('Insurance Premium', 3, 200000.00, 'USD', 'Annual hull insurance', 'INV-2025-005', 4, 4, 'Paid', today - timedelta(days=30)),
        # GOVERNANCE ISSUE: $200k insurance approved by same person who created it
        ('Spare Parts', 5, 32000.00, 'USD', 'Engine spare parts', 'INV-2025-006', 3, 3, 'Pending', today - timedelta(days=2)),
    ]
    
    cursor.executemany('''
        INSERT INTO financial_transactions (transaction_type, vessel_id, amount, currency, 
                                           description, invoice_number, created_by, approved_by, 
                                           payment_status, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', transactions)
    
    print("✓ Seeded 6 financial transactions (with SoD violations)")

def seed_maintenance_records(cursor):
    """Seed maintenance data - GOVERNANCE ISSUE: Same person schedules and completes"""
    today = datetime.now().date()
    maintenance = [
        (1, 'Engine Service', 'Routine engine maintenance', today - timedelta(days=30), 
         today - timedelta(days=28), 2, 2, 15000.00, 'Completed'),
        # GOVERNANCE ISSUE: Same person scheduled and completed
        (2, 'Hull Inspection', 'Annual hull inspection', today - timedelta(days=20), 
         today - timedelta(days=18), 2, 2, 8000.00, 'Completed'),
        (3, 'Safety Equipment', 'Replace life rafts and fire extinguishers', today + timedelta(days=10), 
         None, 2, None, 12000.00, 'Scheduled'),
        (4, 'Propeller Repair', 'Propeller blade damage repair', today - timedelta(days=5), 
         today - timedelta(days=3), 2, 2, 45000.00, 'Completed'),
        # GOVERNANCE ISSUE: $45k maintenance, same person scheduled and completed
        (5, 'Navigation System', 'GPS and radar system upgrade', today + timedelta(days=15), 
         None, 2, None, 25000.00, 'Scheduled'),
    ]
    
    cursor.executemany('''
        INSERT INTO maintenance_records (vessel_id, maintenance_type, description, scheduled_date, 
                                        completed_date, scheduled_by, completed_by, cost, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', maintenance)
    
    print("✓ Seeded 5 maintenance records (with SoD violations)")

def seed_compliance_records(cursor):
    """Seed compliance data - GOVERNANCE ISSUE: No enforcement of regulations"""
    today = datetime.now().date()
    compliance = [
        (1, 'IMO', 'SOLAS Chapter V - Safety of Navigation', today - timedelta(days=100), 
         today + timedelta(days=265), 'Compliant', 'Inspector John Doe', 'All safety equipment verified'),
        (2, 'MARPOL', 'Annex I - Oil Pollution Prevention', today - timedelta(days=200), 
         today - timedelta(days=35), 'Overdue', 'Inspector Jane Smith', 'Inspection overdue by 35 days'),
        # GOVERNANCE ISSUE: Overdue inspection but vessel still operating
        (3, 'ISM Code', 'International Safety Management', today - timedelta(days=150), 
         today + timedelta(days=215), 'Compliant', 'Inspector Ahmed Ali', 'Safety management system approved'),
        (4, 'ISPS', 'International Ship and Port Facility Security', today - timedelta(days=400), 
         today - timedelta(days=35), 'Non-Compliant', 'Inspector Maria Garcia', 'Security measures inadequate'),
        # GOVERNANCE ISSUE: Non-compliant but no action taken
        (5, 'MLC', 'Maritime Labour Convention', today - timedelta(days=180), 
         today + timedelta(days=185), 'Compliant', 'Inspector Robert Brown', 'Crew welfare standards met'),
    ]
    
    cursor.executemany('''
        INSERT INTO compliance_records (vessel_id, compliance_type, regulation_reference, 
                                       inspection_date, next_inspection_due, status, 
                                       inspector_name, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', compliance)
    
    print("✓ Seeded 5 compliance records (with enforcement gaps)")

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        print(f"⚠️  Database {DB_PATH} already exists. Delete it first to reinitialize.")
        response = input("Delete and recreate? (yes/no): ")
        if response.lower() == 'yes':
            os.remove(DB_PATH)
            init_database()
    else:
        init_database()

# Made with Bob
