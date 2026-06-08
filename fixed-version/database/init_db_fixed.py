"""
Initialize XT Shipping Database (FIXED VERSION)
Creates database with proper security and sample data
"""

import sqlite3
import bcrypt
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = 'xt_shipping_fixed.db'
SCHEMA_PATH = 'database/schema_fixed.sql'

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def init_database():
    """Initialize database with schema and sample data"""
    
    # Remove existing database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database: {DB_PATH}")
    
    # Create new database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    print("Database schema created successfully")
    
    # Insert users with hashed passwords
    print("\nCreating users...")
    users = [
        ('admin', '0000', 'admin', 'IT', 'admin@xtshipping.com'),
    ]
    
    for username, password, role, dept, email in users:
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, department, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, role, dept, email))
        print(f"  Created user: {username} (role: {role})")
    
    conn.commit()
    
    # Insert vessels
    print("\nCreating vessels...")
    vessels = [
        ('XT Navigator', 'IMO9876543', 'Container Ship', 'Panama', 50000, 2015, 'Active',
         '2025-01-15', '2026-01-15', '2026-12-31', 'Maritime Insurance Co', 'POL-2025-001'),
        ('XT Explorer', 'IMO9876544', 'Bulk Carrier', 'Liberia', 75000, 2018, 'Active',
         '2025-03-20', '2026-03-20', '2026-06-30', 'Ocean Shield Insurance', 'POL-2025-002'),
        ('XT Voyager', 'IMO9876545', 'Tanker', 'Marshall Islands', 100000, 2020, 'Active',
         '2025-02-10', '2026-02-10', '2025-12-15', 'Global Marine Insurance', 'POL-2024-003'),  # Expiring soon
        ('XT Pioneer', 'IMO9876546', 'Container Ship', 'Singapore', 45000, 2012, 'Active',
         '2024-12-01', '2025-12-01', '2025-11-30', 'Maritime Insurance Co', 'POL-2024-004'),  # Expired
        ('XT Horizon', 'IMO9876547', 'Ro-Ro Vessel', 'Malta', 30000, 2019, 'Maintenance',
         '2025-04-15', '2026-04-15', '2027-03-31', 'Ocean Shield Insurance', 'POL-2025-005'),
    ]
    
    for vessel_data in vessels:
        cursor.execute('''
            INSERT INTO vessels (vessel_name, imo_number, vessel_type, flag_state, gross_tonnage,
                               year_built, status, last_inspection_date, next_inspection_due,
                               insurance_expiry, insurance_provider, insurance_policy_number, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', vessel_data)
        print(f"  Created vessel: {vessel_data[0]}")
    
    conn.commit()
    
    # Insert crew members
    print("\nCreating crew members...")
    crew_members = [
        ('Captain James Wilson', 'Master', 1, 'UK', 'GB123456', 'CERT-001', 'Master Mariner',
         '2027-06-30', '2024-01-01', '2026-12-31', 180, 'Active'),
        ('Chief Engineer Maria Santos', 'Chief Engineer', 1, 'Philippines', 'PH789012', 'CERT-002',
         'Chief Engineer', '2025-10-15', '2024-02-01', '2026-01-31', 195, 'Active'),  # Expiring soon
        ('First Officer David Chen', 'First Officer', 2, 'China', 'CN345678', 'CERT-003',
         'Officer of the Watch', '2024-11-30', '2024-03-01', '2025-12-31', 210, 'Active'),  # Expired cert, excessive hours
        ('Second Engineer Anna Kowalski', 'Second Engineer', 2, 'Poland', 'PL901234', 'CERT-004',
         'Second Engineer', '2026-08-20', '2024-04-01', '2026-03-31', 175, 'Active'),
        ('Bosun Mohammed Al-Rashid', 'Bosun', 3, 'UAE', 'AE567890', 'CERT-005', 'Able Seaman',
         '2026-12-15', '2024-05-01', '2025-11-30', 160, 'Active'),
        ('AB Seaman John Smith', 'Able Seaman', 3, 'USA', 'US234567', 'CERT-006', 'Able Seaman',
         '2024-09-30', '2024-06-01', '2025-12-31', 220, 'Active'),  # Expired cert, excessive hours
    ]
    
    for crew_data in crew_members:
        cursor.execute('''
            INSERT INTO crew (full_name, position, vessel_id, nationality, passport_number,
                            certificate_number, certificate_type, certificate_expiry,
                            contract_start, contract_end, hours_worked_this_month, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', crew_data)
        print(f"  Created crew: {crew_data[0]}")
    
    conn.commit()
    
    # Insert cargo shipments (demonstrating approval workflow)
    print("\nCreating cargo shipments...")
    cargo_shipments = [
        (1, 'Electronics', 'Consumer electronics and components', 500, 'Shanghai', 'Rotterdam',
         '2025-06-01', '2025-06-20', 'Approved', 0, None, 2, 1),  # Created by fleet_manager, approved by admin
        (2, 'Grain', 'Wheat and barley', 15000, 'New Orleans', 'Lagos',
         '2025-06-05', '2025-07-10', 'In Transit', 0, None, 2, 1),
        (3, 'Chemicals', 'Industrial chemicals - Class 8 Corrosive', 800, 'Houston', 'Singapore',
         '2025-06-10', '2025-07-05', 'Pending Approval', 1, 'Class 8', 3, None),  # Dangerous goods, pending
        (1, 'Machinery', 'Heavy machinery and parts', 1200, 'Hamburg', 'Dubai',
         '2025-06-15', '2025-07-10', 'Approved', 0, None, 4, 1),
        (4, 'Automobiles', 'New vehicles for export', 300, 'Tokyo', 'Los Angeles',
         '2025-06-20', '2025-07-15', 'Pending Approval', 0, None, 5, None),  # Pending approval
    ]
    
    for cargo_data in cargo_shipments:
        cursor.execute('''
            INSERT INTO cargo (vessel_id, cargo_type, description, weight_tons, origin_port,
                             destination_port, loading_date, estimated_arrival, status,
                             dangerous_goods, imdg_class, created_by, approved_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', cargo_data)
        print(f"  Created cargo: {cargo_data[1]}")
    
    conn.commit()
    
    # Insert financial transactions (demonstrating approval workflow)
    print("\nCreating financial transactions...")
    transactions = [
        ('Fuel', 1, 45000.00, 'USD', 'Bunker fuel purchase - Singapore', 'INV-2025-001',
         3, 1, 'Approved', '2025-06-01'),  # Created by finance_mgr, approved by admin
        ('Maintenance', 2, 125000.00, 'USD', 'Engine overhaul and repairs', 'INV-2025-002',
         2, 1, 'Approved', '2025-06-05'),  # Created by fleet_manager, approved by admin
        ('Port Fees', 3, 8500.00, 'USD', 'Port charges - Houston', 'INV-2025-003',
         3, 1, 'Paid', '2025-06-10'),
        ('Crew Salary', 1, 75000.00, 'USD', 'Monthly crew salaries', 'INV-2025-004',
         3, None, 'Pending Approval', '2025-06-15'),  # Pending approval
        ('Insurance', 4, 200000.00, 'USD', 'Annual hull and machinery insurance', 'INV-2025-005',
         3, None, 'Pending Approval', '2025-06-20'),  # Large amount, requires dual auth
    ]
    
    for trans_data in transactions:
        cursor.execute('''
            INSERT INTO financial_transactions (transaction_type, vessel_id, amount, currency,
                                              description, invoice_number, created_by, approved_by,
                                              payment_status, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', trans_data)
        print(f"  Created transaction: {trans_data[0]} - ${trans_data[2]:,.2f}")
    
    conn.commit()
    
    # Insert compliance records
    print("\nCreating compliance records...")
    compliance_records = [
        (1, 'SOLAS', 'SOLAS Chapter I - General Provisions', '2025-01-15', '2026-01-15',
         'Compliant', 'Inspector John Doe', 'IMO Inspection Services', 'All safety equipment verified'),
        (2, 'MARPOL', 'MARPOL Annex VI - Air Pollution', '2025-03-20', '2026-03-20',
         'Compliant', 'Inspector Jane Smith', 'Environmental Maritime Agency', 'Emissions within limits'),
        (3, 'ISM Code', 'International Safety Management Code', '2025-02-10', '2026-02-10',
         'Compliant', 'Inspector Robert Brown', 'Classification Society', 'SMS audit passed'),
        (4, 'ISPS', 'International Ship and Port Facility Security', '2024-12-01', '2025-12-01',
         'Overdue', 'Inspector Maria Garcia', 'Port State Control', 'Inspection overdue'),
        (5, 'MLC', 'Maritime Labour Convention', '2025-04-15', '2026-04-15',
         'Compliant', 'Inspector Ahmed Hassan', 'Flag State Administration', 'Crew welfare standards met'),
    ]
    
    for comp_data in compliance_records:
        cursor.execute('''
            INSERT INTO compliance_records (vessel_id, compliance_type, regulation_reference,
                                          inspection_date, next_inspection_due, status,
                                          inspector_name, inspector_organization, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', comp_data)
        print(f"  Created compliance record: {comp_data[1]} for vessel {comp_data[0]}")
    
    conn.commit()
    
    # Insert some activity logs
    print("\nCreating activity logs...")
    log_entries = [
        (1, 'LOGIN_SUCCESS', 'users', 1, 'Admin login', '127.0.0.1', 'Mozilla/5.0'),
        (2, 'CREATE_CARGO', 'cargo', 1, 'Created electronics cargo shipment', '127.0.0.1', 'Mozilla/5.0'),
        (1, 'APPROVE_CARGO', 'cargo', 1, 'Approved cargo shipment', '127.0.0.1', 'Mozilla/5.0'),
        (3, 'CREATE_TRANSACTION', 'financial_transactions', 1, 'Created fuel purchase transaction', '127.0.0.1', 'Mozilla/5.0'),
        (1, 'APPROVE_TRANSACTION', 'financial_transactions', 1, 'Approved fuel purchase', '127.0.0.1', 'Mozilla/5.0'),
    ]
    
    for log_data in log_entries:
        # Create hash for integrity
        log_hash = hash_password(f"{log_data[0]}:{log_data[1]}:{log_data[2]}:{log_data[3]}:{datetime.now().isoformat()}")
        cursor.execute('''
            INSERT INTO activity_log (user_id, action, table_name, record_id, details,
                                    ip_address, user_agent, log_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*log_data, log_hash))
    
    print(f"  Created {len(log_entries)} activity log entries")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database initialized successfully: {DB_PATH}")
    print("\n📋 Default Admin Credentials:")
    print("=" * 60)
    print(f"  Username: admin")
    print(f"  Password: 0000")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Change password on first login!")
    print(f"\n🚀 Start the application with: python app_fixed.py")

if __name__ == '__main__':
    init_database()

# Made with Bob
