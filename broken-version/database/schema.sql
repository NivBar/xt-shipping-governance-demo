-- XT Shipping Management System Database Schema
-- GOVERNANCE ISSUE: No data retention policies defined
-- GOVERNANCE ISSUE: No audit trail tables for critical operations

-- Users table - GOVERNANCE ISSUE: Weak role model, shared credentials
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,  -- SECURITY ISSUE: Plaintext passwords
    role TEXT NOT NULL,      -- GOVERNANCE ISSUE: Simple role, no hierarchy
    department TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- GOVERNANCE ISSUE: No last_login, no password_changed_at
    -- GOVERNANCE ISSUE: No account_locked, no failed_login_attempts
);

-- Vessels table
CREATE TABLE IF NOT EXISTS vessels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_name TEXT NOT NULL,
    imo_number TEXT UNIQUE NOT NULL,
    vessel_type TEXT NOT NULL,
    flag_state TEXT,
    gross_tonnage INTEGER,
    year_built INTEGER,
    status TEXT DEFAULT 'Active',
    -- GOVERNANCE ISSUE: No certification tracking
    last_inspection_date DATE,
    next_inspection_due DATE,
    insurance_expiry DATE,  -- GOVERNANCE ISSUE: No alerts for expiry
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- GOVERNANCE ISSUE: No created_by, modified_by fields
);

-- Cargo table
CREATE TABLE IF NOT EXISTS cargo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_id INTEGER,
    cargo_type TEXT NOT NULL,
    description TEXT,
    weight_tons REAL,
    origin_port TEXT,
    destination_port TEXT,
    loading_date DATE,
    estimated_arrival DATE,
    status TEXT DEFAULT 'In Transit',
    dangerous_goods BOOLEAN DEFAULT 0,  -- GOVERNANCE ISSUE: No compliance checks
    customs_cleared BOOLEAN DEFAULT 0,
    created_by INTEGER,  -- GOVERNANCE ISSUE: No foreign key constraint
    approved_by INTEGER, -- GOVERNANCE ISSUE: Same person can create and approve
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vessel_id) REFERENCES vessels(id)
    -- GOVERNANCE ISSUE: No approval workflow, no segregation of duties
);

-- Crew table
CREATE TABLE IF NOT EXISTS crew (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    position TEXT NOT NULL,
    vessel_id INTEGER,
    nationality TEXT,
    passport_number TEXT,
    certificate_number TEXT,
    certificate_expiry DATE,  -- GOVERNANCE ISSUE: No validation of expiry
    contract_start DATE,
    contract_end DATE,
    hours_worked_this_month INTEGER DEFAULT 0,  -- GOVERNANCE ISSUE: No legal limit enforcement
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vessel_id) REFERENCES vessels(id)
    -- GOVERNANCE ISSUE: No audit trail of assignments
);

-- Financial transactions table
CREATE TABLE IF NOT EXISTS financial_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL,
    vessel_id INTEGER,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    description TEXT,
    invoice_number TEXT,
    created_by INTEGER,
    approved_by INTEGER,  -- GOVERNANCE ISSUE: Can be same as created_by
    payment_status TEXT DEFAULT 'Pending',
    transaction_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vessel_id) REFERENCES vessels(id)
    -- GOVERNANCE ISSUE: No dual authorization requirement
    -- GOVERNANCE ISSUE: No retention policy (required 7 years)
);

-- Maintenance records
CREATE TABLE IF NOT EXISTS maintenance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_id INTEGER NOT NULL,
    maintenance_type TEXT NOT NULL,
    description TEXT,
    scheduled_date DATE,
    completed_date DATE,
    scheduled_by INTEGER,
    completed_by INTEGER,  -- GOVERNANCE ISSUE: Can be same person
    cost REAL,
    status TEXT DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vessel_id) REFERENCES vessels(id)
    -- GOVERNANCE ISSUE: No approval workflow for high-cost maintenance
);

-- Compliance records - GOVERNANCE ISSUE: Incomplete implementation
CREATE TABLE IF NOT EXISTS compliance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_id INTEGER,
    compliance_type TEXT NOT NULL,  -- IMO, SOLAS, MARPOL, etc.
    regulation_reference TEXT,
    inspection_date DATE,
    next_inspection_due DATE,
    status TEXT DEFAULT 'Compliant',
    inspector_name TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vessel_id) REFERENCES vessels(id)
    -- GOVERNANCE ISSUE: No enforcement mechanism
    -- GOVERNANCE ISSUE: No alerts for non-compliance
);

-- Activity log - GOVERNANCE ISSUE: Incomplete audit trail
CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    table_name TEXT,
    record_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- GOVERNANCE ISSUE: Users can delete their own logs
    -- GOVERNANCE ISSUE: No immutability, no cryptographic signing
    -- GOVERNANCE ISSUE: Critical operations not logged
);

-- Insert default admin user - SECURITY ISSUE: Hardcoded credentials
INSERT OR IGNORE INTO users (id, username, password, role, department) VALUES 
(1, 'admin', 'admin123', 'admin', 'IT'),
(2, 'fleet_manager', 'fleet123', 'manager', 'Fleet Operations'),
(3, 'clerk', 'clerk123', 'clerk', 'Administration'),
(4, 'finance', 'finance123', 'finance', 'Finance');
-- GOVERNANCE ISSUE: Shared credentials across departments
-- SECURITY ISSUE: Plaintext passwords in database

-- Made with Bob
