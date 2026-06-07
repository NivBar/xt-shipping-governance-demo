# Governance Issues Documentation

This document provides a comprehensive catalog of all intentional governance and security issues in the XT Shipping Management System demo.

## 📊 Issue Distribution

- **Governance Issues (Primary):** 60-70%
- **Security Issues (Secondary):** 30-40%

---

## 🚨 GOVERNANCE ISSUES (Primary Focus)

### 1. Role-Based Access Control (RBAC) Violations

#### Issue 1.1: No Role Separation
**Severity:** CRITICAL  
**Location:** All routes in `app.py`  
**Description:** All authenticated users can access all features regardless of their role.

**Evidence:**
- Clerk can view financial transactions
- Fleet manager can approve financial transactions
- No role-based filtering of data
- No route protection based on roles

**Impact:**
- Unauthorized access to sensitive data
- Compliance violations (SOX, GDPR)
- Insider threat risk

**Proper Implementation:**
```python
@app.route('/financial')
@require_role(['admin', 'finance'])  # Should restrict access
def financial():
    # Only admin and finance roles should access
```

---

#### Issue 1.2: Shared Credentials
**Severity:** HIGH  
**Location:** `database/schema.sql` lines 147-154  
**Description:** Default credentials are shared and well-known.

**Evidence:**
```sql
INSERT INTO users VALUES 
(1, 'admin', 'admin123', 'admin', 'IT'),
(2, 'fleet_manager', 'fleet123', 'manager', 'Fleet Operations');
```

**Impact:**
- No accountability for actions
- Cannot trace who performed operations
- Violates audit requirements

---

#### Issue 1.3: No Principle of Least Privilege
**Severity:** HIGH  
**Location:** Throughout application  
**Description:** Users have more permissions than needed for their job function.

**Impact:**
- Increased attack surface
- Accidental data modification
- Compliance violations

---

### 2. Segregation of Duties (SoD) Violations

#### Issue 2.1: Self-Approval of Cargo
**Severity:** CRITICAL  
**Location:** `app.py` lines 235-260 (`create_cargo` function)  
**Description:** Same user is set as both creator and approver of cargo shipments.

**Evidence:**
```python
user_id = session['user_id']
cursor.execute('''
    INSERT INTO cargo (..., created_by, approved_by, ...)
    VALUES (..., ?, ?, ...)
''', (..., user_id, user_id, ...))  # Same user!
```

**Impact:**
- Fraud risk - user can approve their own dangerous goods
- No oversight for hazardous materials
- Violates maritime safety regulations

**Proper Implementation:**
- Separate creation and approval roles
- Require different users for approval
- Implement approval workflow

---

#### Issue 2.2: Self-Approval of Financial Transactions
**Severity:** CRITICAL  
**Location:** `app.py` lines 320-350 (`create_transaction` function)  
**Description:** Same user creates and approves financial transactions of any amount.

**Evidence:**
```python
user_id = session['user_id']
cursor.execute('''
    INSERT INTO financial_transactions 
    (..., created_by, approved_by, ...)
    VALUES (..., ?, ?, ...)
''', (..., user_id, user_id, ...))  # Same user approves!
```

**Impact:**
- Fraud risk - embezzlement possible
- No financial controls
- SOX compliance violation
- No dual authorization for large amounts

**Proper Implementation:**
- Transactions >$50,000 require dual authorization
- Creator cannot be approver
- Implement approval workflow with notifications

---

#### Issue 2.3: Maintenance Self-Completion
**Severity:** MEDIUM  
**Location:** `database/init_db.py` lines 145-160  
**Description:** Same person schedules and marks maintenance as complete.

**Impact:**
- Maintenance may not be actually performed
- Safety risk for vessels
- Insurance claim issues

---

### 3. Audit Trail Deficiencies

#### Issue 3.1: Deletable Audit Logs
**Severity:** CRITICAL  
**Location:** `app.py` lines 380-395 (`delete_log` function)  
**Description:** Users can delete audit log entries.

**Evidence:**
```python
@app.route('/api/delete_log/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    # No validation, any user can delete any log
    cursor.execute('DELETE FROM activity_log WHERE id = ?', (log_id,))
```

**Impact:**
- Evidence tampering
- Compliance violations (SOX, HIPAA, GDPR)
- Cannot investigate incidents
- Legal liability

**Proper Implementation:**
- Audit logs must be immutable
- Store in append-only database
- Cryptographically sign each entry
- Separate audit log storage

---

#### Issue 3.2: Incomplete Logging
**Severity:** HIGH  
**Location:** Throughout `app.py`  
**Description:** Critical operations are not logged.

**Missing Logs:**
- Login attempts (successful and failed)
- Approval actions
- Data deletions
- Configuration changes
- Role changes
- Financial transaction approvals

**Impact:**
- Cannot detect unauthorized access
- Cannot investigate incidents
- Compliance violations

---

#### Issue 3.3: Insufficient Log Detail
**Severity:** MEDIUM  
**Location:** `app.py` `log_activity` function  
**Description:** Logs missing critical information.

**Missing Data:**
- IP address
- User agent
- Session ID
- Before/after values
- Detailed action parameters

**Proper Implementation:**
```python
def log_activity(user_id, action, table_name, record_id, 
                ip_address, user_agent, before_value, after_value):
    # Log comprehensive audit trail
```

---

### 4. Data Retention Policy Violations

#### Issue 4.1: No Retention Policies Defined
**Severity:** HIGH  
**Location:** `database/schema.sql`  
**Description:** No data retention policies in database schema.

**Impact:**
- Financial records not retained (7-year legal requirement)
- Crew certifications deleted prematurely
- Voyage logs not archived per maritime law
- Compliance violations

**Proper Implementation:**
```sql
CREATE TABLE financial_transactions (
    ...
    retention_until DATE NOT NULL DEFAULT date('now', '+7 years'),
    archived BOOLEAN DEFAULT 0,
    ...
);
```

---

#### Issue 4.2: No Archival Process
**Severity:** MEDIUM  
**Location:** Application-wide  
**Description:** No automated archival of old records.

**Impact:**
- Database grows indefinitely
- Performance degradation
- Cannot meet legal discovery requests

---

### 5. Compliance Gaps

#### Issue 5.1: Expired Insurance Not Blocked
**Severity:** CRITICAL  
**Location:** `app.py` fleet management  
**Description:** Vessels with expired insurance remain "Active" and operational.

**Evidence:**
- Vessel "XT Navigator" has insurance expired since 2024-03-15
- Still marked as "Active" in database
- No automatic status change

**Impact:**
- Legal liability if vessel operates
- Insurance claims denied
- Maritime law violations

**Proper Implementation:**
- Automatic status change to "Grounded" when insurance expires
- Alerts 30/60/90 days before expiry
- Block vessel assignment to new cargo

---

#### Issue 5.2: Expired Crew Certificates Not Blocked
**Severity:** CRITICAL  
**Location:** `database/init_db.py` crew data  
**Description:** Crew members work with expired certificates.

**Evidence:**
- Chief Engineer Maria Santos: certificate expired 30 days ago
- AB Seaman John Smith: certificate expired 10 days ago
- Both still marked as "Active"

**Impact:**
- Maritime law violations
- Safety risk
- Insurance voidance
- Port state control detention

**Proper Implementation:**
- Automatic suspension when certificate expires
- Alerts before expiry
- Block crew assignment to vessels

---

#### Issue 5.3: Working Hours Exceed Legal Limits
**Severity:** HIGH  
**Location:** `database/init_db.py` crew data  
**Description:** Crew working beyond 200 hours/month legal limit.

**Evidence:**
- Captain James Wilson: 220 hours
- Second Engineer Li Wei: 240 hours (SEVERE violation)

**Impact:**
- Maritime Labour Convention violations
- Crew fatigue - safety risk
- Fines and penalties
- Vessel detention

**Proper Implementation:**
- Hard limit at 200 hours/month
- Alerts at 180 hours
- Block additional assignments
- Automated reporting to authorities

---

#### Issue 5.4: Overdue Inspections Not Blocked
**Severity:** HIGH  
**Location:** Compliance records  
**Description:** Vessels with overdue inspections continue operating.

**Evidence:**
- MARPOL inspection overdue by 35 days
- Vessel still operational

**Impact:**
- Regulatory violations
- Fines and penalties
- Vessel detention at ports

---

#### Issue 5.5: Non-Compliant Vessels Operational
**Severity:** HIGH  
**Location:** Compliance dashboard  
**Description:** Vessels marked "Non-Compliant" still active.

**Evidence:**
- Vessel with "Non-Compliant" ISPS status
- Still marked as "Active"

**Impact:**
- Security risks
- Port access denied
- Regulatory penalties

---

### 6. Domain-Specific Maritime Issues

#### Issue 6.1: No IMO Compliance Tracking
**Severity:** MEDIUM  
**Location:** Compliance module  
**Description:** Incomplete tracking of IMO regulations.

**Missing:**
- SOLAS Chapter requirements
- MARPOL Annexes I-VI
- ISM Code compliance
- ISPS Code compliance

---

#### Issue 6.2: Dangerous Goods Approval
**Severity:** HIGH  
**Location:** Cargo creation  
**Description:** Dangerous goods can be approved by single person.

**Impact:**
- Safety risk
- IMDG Code violations
- Port restrictions

**Proper Implementation:**
- Require certified dangerous goods handler approval
- Dual authorization
- Compatibility checks with other cargo

---

#### Issue 6.3: No Port State Control Integration
**Severity:** MEDIUM  
**Location:** Application-wide  
**Description:** No integration with port state control systems.

**Impact:**
- Cannot verify vessel clearances
- Detention risk at ports

---

## 🔒 SECURITY ISSUES (Secondary Focus)

### S1. SQL Injection
**Severity:** CRITICAL  
**Location:** `app.py` lines 155-160 (login), lines 200-205 (fleet search)  

**Evidence:**
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

**Exploit:**
```
Username: admin' OR '1'='1' --
Password: anything
```

**Fix:** Use parameterized queries

---

### S2. Hardcoded Credentials
**Severity:** HIGH  
**Location:** `app.py` line 13, `database/schema.sql`  

**Evidence:**
```python
app.secret_key = 'xt-shipping-secret-key-2025'
DB_PATH = 'xt_shipping.db'
```

**Fix:** Use environment variables

---

### S3. Plaintext Passwords
**Severity:** CRITICAL  
**Location:** Database schema  

**Evidence:**
```sql
password TEXT NOT NULL,  -- Plaintext!
```

**Fix:** Use bcrypt or Argon2 hashing

---

### S4. No CSRF Protection
**Severity:** HIGH  
**Location:** All forms  

**Fix:** Implement CSRF tokens

---

### S5. Debug Mode Enabled
**Severity:** HIGH  
**Location:** `app.py` line 449  

**Evidence:**
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

**Fix:** Disable debug in production

---

### S6. No Session Timeout
**Severity:** MEDIUM  
**Location:** Session configuration  

**Fix:** Set session timeout (e.g., 30 minutes)

---

## 📈 Summary Statistics

| Category | Critical | High | Medium | Total |
|----------|----------|------|--------|-------|
| Governance | 6 | 8 | 4 | 18 |
| Security | 3 | 3 | 1 | 7 |
| **Total** | **9** | **11** | **5** | **25** |

---

## 🎯 Remediation Priority

### Phase 1 (Immediate - Critical Issues)
1. Fix SQL injection vulnerabilities
2. Implement segregation of duties for financial transactions
3. Make audit logs immutable
4. Block expired insurance/certificates
5. Implement RBAC

### Phase 2 (High Priority)
1. Add approval workflows
2. Implement data retention policies
3. Fix working hours enforcement
4. Add comprehensive logging
5. Hash passwords

### Phase 3 (Medium Priority)
1. Add CSRF protection
2. Implement session timeouts
3. Add dangerous goods controls
4. Improve compliance tracking
5. Add archival processes

---

## 📚 References

- **SOX Compliance:** Sarbanes-Oxley Act requirements
- **GDPR:** General Data Protection Regulation
- **IMO:** International Maritime Organization standards
- **SOLAS:** Safety of Life at Sea Convention
- **MARPOL:** Marine Pollution Convention
- **MLC:** Maritime Labour Convention
- **ISPS:** International Ship and Port Facility Security Code

---

**Document Version:** 1.0  
**Last Updated:** 2025-06-07  
**For:** XT Group Governance Training