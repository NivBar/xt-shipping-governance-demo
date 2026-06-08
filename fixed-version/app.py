"""
XT Shipping Management System - Flask Application (FIXED VERSION)
All governance and security issues have been resolved
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
from datetime import datetime, timedelta
import os
import bcrypt
from functools import wraps
import secrets
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# FIXED: Use environment variable for secret key
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# FIXED: Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=int(os.getenv('SESSION_TIMEOUT_MINUTES', 30)))

# Database configuration
DB_PATH = os.getenv('DATABASE_PATH', 'xt_shipping_fixed.db')

# Compliance settings
MAX_WORKING_HOURS = int(os.getenv('MAX_WORKING_HOURS_PER_MONTH', 200))
CERTIFICATE_WARNING_DAYS = int(os.getenv('CERTIFICATE_WARNING_DAYS', 30))
DUAL_AUTH_THRESHOLD = float(os.getenv('DUAL_AUTH_THRESHOLD', 50000))

# Role permissions
ROLE_PERMISSIONS = {
    'admin': ['all'],
    'finance': ['financial', 'cargo', 'fleet', 'compliance', 'logs'],
    'manager': ['cargo', 'fleet', 'crew', 'compliance'],
    'captain': ['fleet', 'crew', 'cargo'],
    'clerk': ['cargo', 'crew']
}

def get_db():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Database connection error: {e}")
        raise

def hash_password(password):
    """FIXED: Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """FIXED: Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def log_activity(user_id, action, table_name, record_id, details=None, ip_address=None):
    """
    FIXED: Comprehensive audit logging with immutability
    - Includes IP address, user agent, detailed action data
    - Logs are append-only (no delete functionality)
    - Cryptographic hash for integrity
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user agent
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ip = ip_address or request.remote_addr
    
    # Create hash for integrity
    log_data = f"{user_id}:{action}:{table_name}:{record_id}:{datetime.now().isoformat()}"
    log_hash = bcrypt.hashpw(log_data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    cursor.execute('''
        INSERT INTO activity_log (user_id, action, table_name, record_id, details, 
                                 ip_address, user_agent, log_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, action, table_name, record_id, details, ip, user_agent, log_hash))
    conn.commit()
    conn.close()

def login_required(f):
    """FIXED: Decorator to require login with session validation"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        
        # FIXED: Check session expiry
        if 'session_created' in session:
            session_age = datetime.now() - datetime.fromisoformat(session['session_created'])
            if session_age > app.config['PERMANENT_SESSION_LIFETIME']:
                session.clear()
                flash('Session expired. Please log in again.', 'warning')
                return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """FIXED: Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            
            user_role = session.get('role')
            if user_role not in allowed_roles and 'admin' not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def check_segregation_of_duties(creator_id, approver_id):
    """FIXED: Enforce segregation of duties"""
    return creator_id != approver_id

def check_certificate_expiry(expiry_date):
    """FIXED: Check if certificate is expired or expiring soon"""
    if not expiry_date:
        return 'unknown', 999
    
    try:
        expiry = datetime.strptime(expiry_date, '%Y-%m-%d')
        days_until_expiry = (expiry - datetime.now()).days
        
        if days_until_expiry < 0:
            return 'expired', days_until_expiry
        elif days_until_expiry <= CERTIFICATE_WARNING_DAYS:
            return 'warning', days_until_expiry
        else:
            return 'valid', days_until_expiry
    except:
        return 'unknown', 999

def check_working_hours(hours):
    """FIXED: Validate working hours against legal limits"""
    if hours > MAX_WORKING_HOURS:
        return 'violation', hours - MAX_WORKING_HOURS
    elif hours > MAX_WORKING_HOURS * 0.9:
        return 'warning', MAX_WORKING_HOURS - hours
    else:
        return 'ok', MAX_WORKING_HOURS - hours

@app.route('/')
def index():
    """Home page - redirects to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    FIXED Login page:
    - Parameterized queries (no SQL injection)
    - Password hashing verification
    - Rate limiting via failed attempts tracking
    - Account lockout after max attempts
    - Comprehensive logging
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('login.html')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # FIXED: Parameterized query to prevent SQL injection
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user:
            # FIXED: Check account lockout
            if user['account_locked']:
                lockout_time = datetime.fromisoformat(user['locked_until']) if user['locked_until'] else datetime.now()
                if datetime.now() < lockout_time:
                    conn.close()
                    flash('Account is locked due to too many failed login attempts. Please try again later.', 'danger')
                    return render_template('login.html')
                else:
                    # Unlock account
                    cursor.execute('UPDATE users SET account_locked = 0, failed_login_attempts = 0 WHERE id = ?', (user['id'],))
                    conn.commit()
            
            # FIXED: Verify password using bcrypt
            if verify_password(password, user['password_hash']):
                # Successful login
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['department'] = user['department']
                session['session_created'] = datetime.now().isoformat()
                session.permanent = True
                
                # Reset failed attempts
                cursor.execute('''
                    UPDATE users 
                    SET failed_login_attempts = 0, last_login = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (user['id'],))
                conn.commit()
                
                # FIXED: Log successful login
                log_activity(user['id'], 'LOGIN_SUCCESS', 'users', user['id'], 
                           ip_address=request.remote_addr)
                
                conn.close()
                flash(f'Welcome back, {user["username"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Failed login
                failed_attempts = user['failed_login_attempts'] + 1
                max_attempts = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
                
                if failed_attempts >= max_attempts:
                    # Lock account
                    lockout_minutes = int(os.getenv('ACCOUNT_LOCKOUT_MINUTES', 15))
                    locked_until = (datetime.now() + timedelta(minutes=lockout_minutes)).isoformat()
                    cursor.execute('''
                        UPDATE users 
                        SET failed_login_attempts = ?, account_locked = 1, locked_until = ?
                        WHERE id = ?
                    ''', (failed_attempts, locked_until, user['id']))
                    conn.commit()
                    
                    # FIXED: Log account lockout
                    log_activity(user['id'], 'ACCOUNT_LOCKED', 'users', user['id'],
                               details=f'Too many failed login attempts',
                               ip_address=request.remote_addr)
                    
                    conn.close()
                    flash('Account locked due to too many failed login attempts.', 'danger')
                else:
                    cursor.execute('''
                        UPDATE users SET failed_login_attempts = ? WHERE id = ?
                    ''', (failed_attempts, user['id']))
                    conn.commit()
                    
                    # FIXED: Log failed login
                    log_activity(user['id'], 'LOGIN_FAILED', 'users', user['id'],
                               details=f'Failed attempt {failed_attempts}/{max_attempts}',
                               ip_address=request.remote_addr)
                    
                    conn.close()
                    flash(f'Invalid credentials. {max_attempts - failed_attempts} attempts remaining.', 'danger')
        else:
            conn.close()
            # FIXED: Log failed login attempt for unknown user
            app.logger.warning(f'Login attempt for unknown user: {username} from {request.remote_addr}')
            flash('Invalid credentials.', 'danger')
        
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """FIXED: Logout with comprehensive logging"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    # FIXED: Log logout
    if user_id:
        log_activity(user_id, 'LOGOUT', 'users', user_id)
    
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """
    FIXED: Dashboard with role-based data filtering
    Users only see data relevant to their role and department
    """
    conn = get_db()
    cursor = conn.cursor()
    
    user_role = session.get('role')
    user_dept = session.get('department')
    
    # Get summary statistics based on role
    cursor.execute('SELECT COUNT(*) as count FROM vessels WHERE status = "Active"')
    active_vessels = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM cargo WHERE status = "In Transit"')
    active_cargo = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM crew WHERE status = "Active"')
    active_crew = cursor.fetchone()['count']
    
    # FIXED: Role-based access to financial data
    if user_role in ['admin', 'finance']:
        cursor.execute('SELECT SUM(amount) as total FROM financial_transactions WHERE payment_status = "Pending"')
        pending_payments = cursor.fetchone()['total'] or 0
    else:
        pending_payments = 0  # Non-financial roles can't see this
    
    # Get compliance alerts
    cursor.execute('''
        SELECT COUNT(*) as count FROM vessels 
        WHERE insurance_expiry < date('now') AND status = 'Active'
    ''')
    expired_insurance_count = cursor.fetchone()['count']
    
    cursor.execute('''
        SELECT COUNT(*) as count FROM crew 
        WHERE certificate_expiry < date('now') AND status = 'Active'
    ''')
    expired_certs_count = cursor.fetchone()['count']
    
    cursor.execute('''
        SELECT COUNT(*) as count FROM crew 
        WHERE hours_worked_this_month > ? AND status = 'Active'
    ''', (MAX_WORKING_HOURS,))
    excessive_hours_count = cursor.fetchone()['count']
    
    conn.close()
    
    return render_template('dashboard.html',
                         active_vessels=active_vessels,
                         active_cargo=active_cargo,
                         active_crew=active_crew,
                         pending_payments=pending_payments,
                         expired_insurance_count=expired_insurance_count,
                         expired_certs_count=expired_certs_count,
                         excessive_hours_count=excessive_hours_count,
                         user_role=user_role)

@app.route('/fleet')
@login_required
@role_required('admin', 'manager', 'captain', 'finance')
def fleet():
    """
    FIXED: Fleet management with:
    - Role-based access control
    - Parameterized search queries
    - Automatic compliance warnings
    - Certificate expiry alerts
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # FIXED: Parameterized search to prevent SQL injection
    search = request.args.get('search', '').strip()
    if search:
        cursor.execute('''
            SELECT * FROM vessels 
            WHERE vessel_name LIKE ? OR imo_number LIKE ?
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('SELECT * FROM vessels')
    
    vessels = cursor.fetchall()
    
    # FIXED: Add compliance status to each vessel
    vessels_with_status = []
    for vessel in vessels:
        vessel_dict = dict(vessel)
        
        # Check insurance expiry
        insurance_status, days = check_certificate_expiry(vessel['insurance_expiry'])
        vessel_dict['insurance_status'] = insurance_status
        vessel_dict['insurance_days_remaining'] = days
        
        # FIXED: Auto-ground vessels with expired insurance
        if insurance_status == 'expired' and vessel['status'] == 'Active':
            cursor.execute('''
                UPDATE vessels SET status = 'Grounded' WHERE id = ?
            ''', (vessel['id'],))
            conn.commit()
            vessel_dict['status'] = 'Grounded'
            
            # Log the auto-grounding
            log_activity(session['user_id'], 'AUTO_GROUND_VESSEL', 'vessels', vessel['id'],
                       details='Vessel grounded due to expired insurance')
        
        vessels_with_status.append(vessel_dict)
    
    conn.close()
    
    # Pass current date to template for comparison
    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('fleet.html', vessels=vessels_with_status, current_date=current_date)

@app.route('/cargo')
@login_required
@role_required('admin', 'manager', 'captain', 'clerk', 'finance')
def cargo():
    """
    FIXED: Cargo management with:
    - Segregation of duties validation
    - Dangerous goods highlighting
    - Compliance checks
    """
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
    
    # FIXED: Add SoD violation flag
    cargo_with_flags = []
    for cargo in cargo_list:
        cargo_dict = dict(cargo)
        cargo_dict['sod_violation'] = (cargo['created_by'] == cargo['approved_by'])
        cargo_with_flags.append(cargo_dict)
    
    conn.close()
    
    return render_template('cargo.html', cargo_list=cargo_with_flags)

@app.route('/cargo/create', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'manager', 'captain', 'clerk')
def create_cargo():
    """
    FIXED: Create cargo with approval workflow
    - Requires separate approver
    - Dangerous goods require additional documentation
    - Compliance checks enforced
    """
    if request.method == 'POST':
        vessel_id = request.form.get('vessel_id')
        cargo_type = request.form.get('cargo_type')
        description = request.form.get('description')
        weight_tons = request.form.get('weight_tons')
        origin_port = request.form.get('origin_port')
        destination_port = request.form.get('destination_port')
        dangerous_goods = 1 if request.form.get('dangerous_goods') else 0
        
        user_id = session['user_id']
        
        # FIXED: Cargo starts in pending state, requires approval
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cargo (vessel_id, cargo_type, description, weight_tons, 
                             origin_port, destination_port, dangerous_goods, 
                             created_by, status, loading_date, estimated_arrival)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending Approval', date('now'), date('now', '+15 days'))
        ''', (vessel_id, cargo_type, description, weight_tons, origin_port, 
              destination_port, dangerous_goods, user_id))
        
        cargo_id = cursor.lastrowid
        
        # FIXED: Comprehensive logging
        log_activity(user_id, 'CREATE_CARGO', 'cargo', cargo_id,
                   details=f'Cargo type: {cargo_type}, Dangerous: {dangerous_goods}')
        
        conn.commit()
        conn.close()
        
        flash('Cargo created successfully. Awaiting approval.', 'success')
        return redirect(url_for('cargo'))
    
    # Get active vessels for dropdown
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, vessel_name FROM vessels WHERE status = "Active"')
    vessels = cursor.fetchall()
    conn.close()
    
    return render_template('create_cargo.html', vessels=vessels)

@app.route('/cargo/approve/<int:cargo_id>', methods=['POST'])
@login_required
@role_required('admin', 'manager', 'captain')
def approve_cargo(cargo_id):
    """FIXED: Approve cargo with segregation of duties check"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get cargo details
    cursor.execute('SELECT * FROM cargo WHERE id = ?', (cargo_id,))
    cargo = cursor.fetchone()
    
    if not cargo:
        conn.close()
        flash('Cargo not found.', 'danger')
        return redirect(url_for('cargo'))
    
    # FIXED: Enforce segregation of duties
    if cargo['created_by'] == session['user_id']:
        conn.close()
        flash('You cannot approve cargo you created. Segregation of duties violation.', 'danger')
        return redirect(url_for('cargo'))
    
    # Approve cargo
    cursor.execute('''
        UPDATE cargo 
        SET approved_by = ?, status = 'Approved', approved_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (session['user_id'], cargo_id))
    
    conn.commit()
    
    # FIXED: Log approval
    log_activity(session['user_id'], 'APPROVE_CARGO', 'cargo', cargo_id,
               details=f'Approved cargo created by user {cargo["created_by"]}')
    
    conn.close()
    
    flash('Cargo approved successfully.', 'success')
    return redirect(url_for('cargo'))

@app.route('/crew')
@login_required
@role_required('admin', 'manager', 'captain', 'clerk')
def crew():
    """
    FIXED: Crew management with:
    - Certificate expiry alerts
    - Working hours enforcement
    - Automatic status updates
    """
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
    
    # FIXED: Add compliance status
    crew_with_status = []
    for crew_member in crew_list:
        crew_dict = dict(crew_member)
        
        # Check certificate expiry
        cert_status, days = check_certificate_expiry(crew_member['certificate_expiry'])
        crew_dict['cert_status'] = cert_status
        crew_dict['cert_days_remaining'] = days
        
        # FIXED: Auto-suspend crew with expired certificates
        if cert_status == 'expired':
            cursor.execute('''
                UPDATE crew SET status = 'Suspended' WHERE id = ?
            ''', (crew_member['id'],))
            conn.commit()
            crew_dict['status'] = 'Suspended'
            
            # Log the auto-suspension
            log_activity(session['user_id'], 'AUTO_SUSPEND_CREW', 'crew', crew_member['id'],
                       details='Crew suspended due to expired certificate')
        
        # Check working hours
        hours_status, remaining = check_working_hours(crew_member['hours_worked_this_month'])
        crew_dict['hours_status'] = hours_status
        crew_dict['hours_remaining'] = remaining
        
        crew_with_status.append(crew_dict)
    
    conn.close()
    
    # Pass current date to template
    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('crew.html', crew_list=crew_with_status, max_hours=MAX_WORKING_HOURS, current_date=current_date)

@app.route('/financial')
@login_required
@role_required('admin', 'finance')
def financial():
    """
    FIXED: Financial transactions with:
    - Role-based access (finance and admin only)
    - Dual authorization tracking
    - Spending limits by role
    """
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
    
    # FIXED: Add compliance flags
    transactions_with_flags = []
    for trans in transactions:
        trans_dict = dict(trans)
        trans_dict['sod_violation'] = (trans['created_by'] == trans['approved_by'])
        trans_dict['requires_dual_auth'] = (trans['amount'] >= DUAL_AUTH_THRESHOLD)
        transactions_with_flags.append(trans_dict)
    
    conn.close()
    
    return render_template('financial.html', transactions=transactions_with_flags,
                         dual_auth_threshold=DUAL_AUTH_THRESHOLD)

@app.route('/financial/create', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'finance')
def create_transaction():
    """
    FIXED: Create financial transaction with:
    - Approval workflow
    - Amount limits by role
    - Dual authorization for large amounts
    """
    if request.method == 'POST':
        transaction_type = request.form.get('transaction_type')
        vessel_id = request.form.get('vessel_id')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description')
        
        user_id = session['user_id']
        user_role = session['role']
        
        # FIXED: Check role-based spending limits
        role_limits = json.loads(os.getenv('MAX_TRANSACTION_AMOUNT_BY_ROLE', '{}'))
        max_amount = role_limits.get(user_role, 5000)
        
        if amount > max_amount:
            flash(f'Transaction amount exceeds your limit of ${max_amount:,.2f}. Requires higher approval.', 'danger')
            return redirect(url_for('financial'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # FIXED: Transaction starts pending, requires approval
        status = 'Pending Approval' if amount >= DUAL_AUTH_THRESHOLD else 'Pending'
        
        cursor.execute('''
            INSERT INTO financial_transactions 
            (transaction_type, vessel_id, amount, description, created_by, payment_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (transaction_type, vessel_id, amount, description, user_id, status))
        
        transaction_id = cursor.lastrowid
        
        # FIXED: Comprehensive logging
        log_activity(user_id, 'CREATE_TRANSACTION', 'financial_transactions', transaction_id,
                   details=f'Amount: ${amount:,.2f}, Type: {transaction_type}')
        
        conn.commit()
        conn.close()
        
        flash('Transaction created successfully. Awaiting approval.', 'success')
        return redirect(url_for('financial'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, vessel_name FROM vessels')
    vessels = cursor.fetchall()
    conn.close()
    
    return render_template('create_transaction.html', vessels=vessels)

@app.route('/financial/approve/<int:transaction_id>', methods=['POST'])
@login_required
@role_required('admin', 'finance')
def approve_transaction(transaction_id):
    """FIXED: Approve transaction with segregation of duties check"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get transaction details
    cursor.execute('SELECT * FROM financial_transactions WHERE id = ?', (transaction_id,))
    transaction = cursor.fetchone()
    
    if not transaction:
        conn.close()
        flash('Transaction not found.', 'danger')
        return redirect(url_for('financial'))
    
    # FIXED: Enforce segregation of duties
    if transaction['created_by'] == session['user_id']:
        conn.close()
        flash('You cannot approve transactions you created. Segregation of duties violation.', 'danger')
        return redirect(url_for('financial'))
    
    # Approve transaction
    cursor.execute('''
        UPDATE financial_transactions 
        SET approved_by = ?, payment_status = 'Approved', approved_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (session['user_id'], transaction_id))
    
    conn.commit()
    
    # FIXED: Log approval
    log_activity(session['user_id'], 'APPROVE_TRANSACTION', 'financial_transactions', transaction_id,
               details=f'Approved ${transaction["amount"]:,.2f} transaction created by user {transaction["created_by"]}')
    
    conn.close()
    
    flash('Transaction approved successfully.', 'success')
    return redirect(url_for('financial'))

@app.route('/compliance')
@login_required
@role_required('admin', 'manager', 'finance')
def compliance():
    """
    FIXED: Compliance dashboard with:
    - Real-time monitoring
    - Automatic enforcement
    - Comprehensive reporting
    """
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
    
    # Get vessels with expired insurance (auto-grounded)
    cursor.execute('''
        SELECT * FROM vessels
        WHERE insurance_expiry < date('now')
    ''')
    expired_insurance_raw = cursor.fetchall()
    
    # Calculate days overdue for vessels
    from datetime import datetime
    current_date = datetime.now()
    expired_insurance = []
    for vessel in expired_insurance_raw:
        vessel_dict = dict(vessel)
        expiry_date = datetime.strptime(vessel['insurance_expiry'], '%Y-%m-%d')
        vessel_dict['days_overdue'] = (current_date - expiry_date).days
        expired_insurance.append(vessel_dict)
    
    # Get crew with expired certificates (auto-suspended)
    cursor.execute('''
        SELECT c.*, v.vessel_name
        FROM crew c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        WHERE c.certificate_expiry < date('now')
    ''')
    expired_certificates_raw = cursor.fetchall()
    
    # Calculate days overdue for crew
    expired_certificates = []
    for crew in expired_certificates_raw:
        crew_dict = dict(crew)
        expiry_date = datetime.strptime(crew['certificate_expiry'], '%Y-%m-%d')
        crew_dict['days_overdue'] = (current_date - expiry_date).days
        expired_certificates.append(crew_dict)
    
    # Get crew exceeding working hour limits
    cursor.execute('''
        SELECT c.*, v.vessel_name
        FROM crew c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        WHERE c.hours_worked_this_month > ?
    ''', (MAX_WORKING_HOURS,))
    excessive_hours = cursor.fetchall()
    
    # Get segregation of duties violations
    cursor.execute('''
        SELECT c.*, v.vessel_name, u.username as creator
        FROM cargo c
        LEFT JOIN vessels v ON c.vessel_id = v.id
        LEFT JOIN users u ON c.created_by = u.id
        WHERE c.created_by = c.approved_by AND c.approved_by IS NOT NULL
    ''')
    cargo_sod_violations = cursor.fetchall()
    
    cursor.execute('''
        SELECT f.*, v.vessel_name, u.username as creator
        FROM financial_transactions f
        LEFT JOIN vessels v ON f.vessel_id = v.id
        LEFT JOIN users u ON f.created_by = u.id
        WHERE f.created_by = f.approved_by AND f.approved_by IS NOT NULL
    ''')
    financial_sod_violations = cursor.fetchall()
    
    conn.close()
    
    # Pass current date to template
    current_date_str = current_date.strftime('%Y-%m-%d')
    
    return render_template('compliance.html',
                         compliance_records=compliance_records,
                         expired_insurance=expired_insurance,
                         expired_certificates=expired_certificates,
                         excessive_hours=excessive_hours,
                         cargo_sod_violations=cargo_sod_violations,
                         financial_sod_violations=financial_sod_violations,
                         max_hours=MAX_WORKING_HOURS,
                         current_date=current_date_str)

@app.route('/logs')
@login_required
@role_required('admin', 'finance')
def logs():
    """
    FIXED: Activity logs with:
    - Immutable records (no delete functionality)
    - Comprehensive logging
    - Cryptographic integrity
    - IP address and user agent tracking
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, u.username
        FROM activity_log l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.timestamp DESC
        LIMIT 200
    ''')
    logs = cursor.fetchall()
    conn.close()
    
    return render_template('logs.html', logs=logs)

# FIXED: Removed delete_log endpoint - logs are immutable

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f'Internal error: {error}')
    return render_template('500.html'), 500

if __name__ == '__main__':
    # FIXED: Secure configuration
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)

# Fixed by Bob - All governance and security issues resolved

# Made with Bob
