"""
XT Shipping Management System - Flask Application
GOVERNANCE DEMO: Contains intentional governance and security issues
For educational purposes only!
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# SECURITY ISSUE: Hardcoded secret key
app.secret_key = 'xt-shipping-secret-key-2025'

# SECURITY ISSUE: Hardcoded database credentials
DB_PATH = 'xt_shipping.db'

# GOVERNANCE ISSUE: No session timeout configuration
# GOVERNANCE ISSUE: No secure session settings

def get_db():
    """Get database connection - GOVERNANCE ISSUE: No connection pooling"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_activity(user_id, action, table_name, record_id):
    """
    Log user activity - GOVERNANCE ISSUE: Incomplete audit trail
    - Missing: IP address, user agent, detailed action data
    - Users can delete their own logs
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activity_log (user_id, action, table_name, record_id)
        VALUES (?, ?, ?, ?)
    ''', (user_id, action, table_name, record_id))
    conn.commit()
    conn.close()

# GOVERNANCE ISSUE: No role-based access control decorator
# All routes accessible by all authenticated users

@app.route('/')
def index():
    """Home page - redirects to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page - SECURITY ISSUES:
    - SQL Injection vulnerability
    - Plaintext password comparison
    - No rate limiting
    - No account lockout
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # SECURITY ISSUE: SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # GOVERNANCE ISSUE: No logging of successful login
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['department'] = user['department']
            # GOVERNANCE ISSUE: No session expiry time set
            return redirect(url_for('dashboard'))
        else:
            # GOVERNANCE ISSUE: No logging of failed login attempts
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout - GOVERNANCE ISSUE: No logout logging"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """
    Main dashboard - GOVERNANCE ISSUE: No role-based access control
    All users see all data regardless of role
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get summary statistics
    cursor.execute('SELECT COUNT(*) as count FROM vessels WHERE status = "Active"')
    active_vessels = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM cargo WHERE status = "In Transit"')
    active_cargo = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM crew WHERE status = "Active"')
    active_crew = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(amount) as total FROM financial_transactions WHERE payment_status = "Pending"')
    pending_payments = cursor.fetchone()['total'] or 0
    
    # GOVERNANCE ISSUE: No filtering based on user role or department
    # Clerk can see financial data, fleet manager can see everything
    
    conn.close()
    
    return render_template('dashboard.html',
                         active_vessels=active_vessels,
                         active_cargo=active_cargo,
                         active_crew=active_crew,
                         pending_payments=pending_payments)

@app.route('/fleet')
def fleet():
    """
    Fleet management - GOVERNANCE ISSUES:
    - No role-based filtering
    - Shows expired certifications without alerts
    - No compliance warnings
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # SECURITY ISSUE: SQL Injection in search
    search = request.args.get('search', '')
    if search:
        # SECURITY ISSUE: Vulnerable to SQL injection
        query = f"SELECT * FROM vessels WHERE vessel_name LIKE '%{search}%' OR imo_number LIKE '%{search}%'"
        cursor.execute(query)
    else:
        cursor.execute('SELECT * FROM vessels')
    
    vessels = cursor.fetchall()
    
    # GOVERNANCE ISSUE: No validation of expired insurance or inspections
    # Data shown as-is without warnings
    
    conn.close()
    
    return render_template('fleet.html', vessels=vessels)

@app.route('/cargo')
def cargo():
    """
    Cargo management - GOVERNANCE ISSUES:
    - No segregation of duties validation
    - Dangerous goods not highlighted
    - Same person can create and approve
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, v.vessel_name, 
               u1.username as created_by_name,
               u2.username as approved_by_name
        FROM cargo c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        LEFT JOIN users u1 ON c.created_by = u1.id
        LEFT JOIN users u2 ON c.approved_by = u2.id
        ORDER BY c.created_at DESC
    ''')
    cargo_list = cursor.fetchall()
    conn.close()
    
    # GOVERNANCE ISSUE: No warning when created_by == approved_by
    # GOVERNANCE ISSUE: Dangerous goods not flagged prominently
    
    return render_template('cargo.html', cargo_list=cargo_list)

@app.route('/cargo/create', methods=['GET', 'POST'])
def create_cargo():
    """
    Create cargo - GOVERNANCE ISSUE: No approval workflow
    User can create and immediately approve their own cargo
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        vessel_id = request.form.get('vessel_id')
        cargo_type = request.form.get('cargo_type')
        description = request.form.get('description')
        weight_tons = request.form.get('weight_tons')
        origin_port = request.form.get('origin_port')
        destination_port = request.form.get('destination_port')
        dangerous_goods = 1 if request.form.get('dangerous_goods') else 0
        
        # GOVERNANCE ISSUE: Same user as creator and approver
        user_id = session['user_id']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cargo (vessel_id, cargo_type, description, weight_tons, 
                             origin_port, destination_port, dangerous_goods, 
                             created_by, approved_by, loading_date, estimated_arrival)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), date('now', '+15 days'))
        ''', (vessel_id, cargo_type, description, weight_tons, origin_port, 
              destination_port, dangerous_goods, user_id, user_id))
        
        cargo_id = cursor.lastrowid
        
        # GOVERNANCE ISSUE: Minimal logging, no approval workflow logged
        log_activity(user_id, 'CREATE_CARGO', 'cargo', cargo_id)
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('cargo'))
    
    # Get vessels for dropdown
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, vessel_name FROM vessels WHERE status = "Active"')
    vessels = cursor.fetchall()
    conn.close()
    
    return render_template('create_cargo.html', vessels=vessels)

@app.route('/crew')
def crew():
    """
    Crew management - GOVERNANCE ISSUES:
    - No alerts for expired certificates
    - No enforcement of working hour limits
    - Shows violations but doesn't prevent them
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, v.vessel_name
        FROM crew c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        WHERE c.status = "Active"
        ORDER BY c.full_name
    ''')
    crew_list = cursor.fetchall()
    conn.close()
    
    # GOVERNANCE ISSUE: No validation or warnings for:
    # - Expired certificates
    # - Excessive working hours (>200 hours/month)
    # - Expired contracts
    
    return render_template('crew.html', crew_list=crew_list)

@app.route('/financial')
def financial():
    """
    Financial transactions - GOVERNANCE ISSUES:
    - No dual authorization requirement
    - Same person can create and approve large amounts
    - No spending limits by role
    - No retention policy enforcement
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # GOVERNANCE ISSUE: Clerk can view all financial data
    # No role-based filtering
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.*, v.vessel_name,
               u1.username as created_by_name,
               u2.username as approved_by_name
        FROM financial_transactions f
        LEFT JOIN vessels v ON f.vessel_id = v.id
        LEFT JOIN users u1 ON f.created_by = u1.id
        LEFT JOIN users u2 ON f.approved_by = u2.id
        ORDER BY f.transaction_date DESC
    ''')
    transactions = cursor.fetchall()
    conn.close()
    
    # GOVERNANCE ISSUE: No warning for same person creating and approving
    # GOVERNANCE ISSUE: No alerts for large transactions without dual auth
    
    return render_template('financial.html', transactions=transactions)

@app.route('/financial/create', methods=['GET', 'POST'])
def create_transaction():
    """
    Create financial transaction - GOVERNANCE ISSUE: No approval workflow
    User can approve their own transactions, even large amounts
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        transaction_type = request.form.get('transaction_type')
        vessel_id = request.form.get('vessel_id')
        amount = request.form.get('amount')
        description = request.form.get('description')
        
        # GOVERNANCE ISSUE: Same user creates and approves
        # No validation of amount limits
        user_id = session['user_id']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO financial_transactions 
            (transaction_type, vessel_id, amount, description, created_by, approved_by, payment_status)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending')
        ''', (transaction_type, vessel_id, amount, description, user_id, user_id))
        
        transaction_id = cursor.lastrowid
        
        # GOVERNANCE ISSUE: No logging of approval, no dual authorization check
        log_activity(user_id, 'CREATE_TRANSACTION', 'financial_transactions', transaction_id)
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('financial'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, vessel_name FROM vessels')
    vessels = cursor.fetchall()
    conn.close()
    
    return render_template('create_transaction.html', vessels=vessels)

@app.route('/compliance')
def compliance():
    """
    Compliance dashboard - GOVERNANCE ISSUES:
    - Shows violations but no enforcement
    - Overdue inspections not blocked
    - Non-compliant vessels still operational
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all compliance records
    cursor.execute('''
        SELECT c.*, v.vessel_name
        FROM compliance_records c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        ORDER BY c.next_inspection_due
    ''')
    compliance_records = cursor.fetchall()
    
    # GOVERNANCE ISSUE: Get vessels with expired insurance (but still operating)
    cursor.execute('''
        SELECT * FROM vessels 
        WHERE insurance_expiry < date('now') AND status = 'Active'
    ''')
    expired_insurance = cursor.fetchall()
    
    # GOVERNANCE ISSUE: Get crew with expired certificates (but still working)
    cursor.execute('''
        SELECT c.*, v.vessel_name
        FROM crew c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        WHERE c.certificate_expiry < date('now') AND c.status = 'Active'
    ''')
    expired_certificates = cursor.fetchall()
    
    # GOVERNANCE ISSUE: Get crew exceeding working hour limits
    cursor.execute('''
        SELECT c.*, v.vessel_name
        FROM crew c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        WHERE c.hours_worked_this_month > 200 AND c.status = 'Active'
    ''')
    excessive_hours = cursor.fetchall()
    
    conn.close()
    
    # GOVERNANCE ISSUE: Data displayed but no enforcement actions
    
    return render_template('compliance.html',
                         compliance_records=compliance_records,
                         expired_insurance=expired_insurance,
                         expired_certificates=expired_certificates,
                         excessive_hours=excessive_hours)

@app.route('/api/delete_log/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    """
    GOVERNANCE ISSUE: Users can delete audit logs!
    This should NEVER be allowed in a real system
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # GOVERNANCE ISSUE: No validation, any user can delete any log
    cursor.execute('DELETE FROM activity_log WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/logs')
def logs():
    """
    Activity logs - GOVERNANCE ISSUES:
    - Incomplete logging (missing critical operations)
    - Users can delete logs
    - No immutability
    - No cryptographic signing
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, u.username
        FROM activity_log l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.timestamp DESC
        LIMIT 100
    ''')
    logs = cursor.fetchall()
    conn.close()
    
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    # SECURITY ISSUE: Debug mode enabled
    # SECURITY ISSUE: Running on all interfaces (0.0.0.0)
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
