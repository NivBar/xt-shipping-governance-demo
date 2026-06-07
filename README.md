# XT Shipping Management System - Governance Demo

⚠️ **WARNING: This application contains intentional governance and security vulnerabilities for educational purposes only!**

## 🌊 About XT Group

XT Group is a global holding group comprised of diverse, innovative and market-leading companies. The Group's story is a classic tale of the founders' journey, the late Sammy and Yuli Ofer, from rags to riches, and now is being managed by the 3rd generation.

At the heart of the Group is XT Shipping, an established leading international ship owner and manager. XT Shipping Group is expanding its fleet and has a well-known reputation for professionalism, quality, and reliability.

**XT's Vision:** To provide customers with the highest standards of Service, Safety, and Efficiency.

## 📋 Project Overview

This is a demonstration Flask web application for XT Group's shipping operations that intentionally contains **governance domain issues** and security vulnerabilities. The primary focus (60-70%) is on governance violations, with security issues as a secondary concern (30-40%).

### Purpose

- Demonstrate common governance failures in enterprise applications
- Showcase domain-specific compliance gaps in maritime operations
- Provide a training platform for identifying and fixing governance issues
- Serve as a foundation for adding proper governance controls

## 🎯 Key Features

- **Fleet Management** - Track vessels, certifications, and insurance
- **Cargo Operations** - Manage shipments and dangerous goods
- **Crew Management** - Personnel records and certifications
- **Financial Operations** - Transactions and payments
- **Compliance Dashboard** - Maritime regulations monitoring
- **Activity Logs** - Audit trail (with intentional issues)

## 🚨 Intentional Governance Issues

### Primary Issues (Governance Domain - 60-70%)

1. **Role-Based Access Control (RBAC) Violations**
   - No role separation - all users see all data
   - Clerk can view financial transactions
   - No principle of least privilege
   - Shared admin credentials

2. **Segregation of Duties (SoD) Failures**
   - Same person can create AND approve cargo shipments
   - Same person can create AND approve financial transactions
   - No dual authorization for large transactions ($50k+)
   - Dangerous goods approved by single person

3. **Audit Trail Deficiencies**
   - Critical operations not logged (approvals, deletions)
   - Users can DELETE audit logs
   - No immutable audit records
   - Missing: IP address, user agent, detailed action data
   - No cryptographic signing of logs

4. **Data Retention Policy Violations**
   - No retention policies defined
   - Financial records not retained (7-year requirement)
   - Crew certifications deleted prematurely
   - Voyage logs not archived per maritime law

5. **Compliance Gaps**
   - IMO regulations not enforced
   - SOLAS requirements bypassed
   - MARPOL environmental compliance not tracked
   - Vessels with expired insurance still operational
   - Crew working with expired certificates
   - Working hours exceed legal limits (>200 hours/month)

6. **Domain-Specific Issues**
   - Expired vessel certifications but still active
   - Insurance policies lapsed but vessels sailing
   - Overdue inspections not blocked
   - Non-compliant vessels still operational

### Secondary Issues (Security - 30-40%)

1. **SQL Injection** - Search functionality vulnerable
2. **Hardcoded Credentials** - Database and admin passwords in code
3. **Plaintext Passwords** - No password hashing
4. **No CSRF Protection** - Forms vulnerable to CSRF attacks
5. **Session Management** - No timeout, insecure settings
6. **Debug Mode Enabled** - Flask debug mode in production

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the repository**
   ```bash
   cd xt-shipping-governance-demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python database/init_db.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser to: `http://localhost:5000`
   - Use one of the demo credentials (see below)

### Demo Credentials

| Username | Password | Role | Department |
|----------|----------|------|------------|
| admin | admin123 | admin | IT |
| fleet_manager | fleet123 | manager | Fleet Operations |
| clerk | clerk123 | clerk | Administration |
| finance | finance123 | finance | Finance |

⚠️ **Note:** All users can access all features - this is a governance issue!

## 📊 Sample Data

The database is pre-populated with:

- **5 Vessels** - Including some with expired insurance/inspections
- **5 Cargo Shipments** - With SoD violations (same creator/approver)
- **6 Crew Members** - Some with expired certificates or excessive hours
- **6 Financial Transactions** - With SoD violations
- **5 Maintenance Records** - Same person schedules and completes
- **5 Compliance Records** - Showing overdue and non-compliant status

## 🔍 Exploring the Issues

### 1. Login with SQL Injection
Try logging in with: `admin' OR '1'='1' --` (username) and any password

### 2. Check Segregation of Duties
- Go to **Cargo** or **Financial** pages
- Look for yellow-highlighted rows where creator = approver

### 3. View Compliance Violations
- Go to **Compliance** dashboard
- See vessels with expired insurance still marked "Active"
- See crew with expired certificates still working
- See crew exceeding 200 hours/month legal limit

### 4. Delete Audit Logs
- Go to **Logs** page
- Click "Delete" button on any log entry
- This should NEVER be possible in a real system!

### 5. Create Self-Approved Transactions
- Go to **Financial** → Create Transaction
- Submit a large transaction (e.g., $100,000)
- You will be both creator AND approver!

## 📁 Project Structure

```
xt-shipping-governance-demo/
├── app.py                          # Flask application (with issues)
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore file
├── README.md                       # This file
├── GOVERNANCE_ISSUES.md            # Detailed issue documentation
├── GITHUB_SETUP.md                 # GitHub connection guide
├── database/
│   ├── init_db.py                  # Database initialization
│   └── schema.sql                  # Database schema
├── static/
│   └── css/
│       └── maritime-theme.css      # Modern maritime UI styling
└── templates/                      # HTML templates
    ├── base.html                   # Base template
    ├── login.html                  # Login page
    ├── dashboard.html              # Main dashboard
    ├── fleet.html                  # Fleet management
    ├── cargo.html                  # Cargo operations
    ├── crew.html                   # Crew management
    ├── financial.html              # Financial operations
    ├── compliance.html             # Compliance dashboard
    ├── logs.html                   # Activity logs
    ├── create_cargo.html           # Create cargo form
    └── create_transaction.html     # Create transaction form
```

## 🎓 Learning Objectives

After exploring this demo, you should understand:

1. **Why RBAC matters** - Not all users should see all data
2. **Segregation of Duties** - Critical operations need multiple approvers
3. **Audit Trail Importance** - Logs must be immutable and complete
4. **Data Retention** - Legal requirements for record keeping
5. **Compliance Enforcement** - Violations must be blocked, not just reported
6. **Domain-Specific Governance** - Maritime industry has unique requirements

## 🔧 Next Steps

This demo is designed to be a starting point. Future enhancements could include:

1. **Fix Governance Issues** - Implement proper RBAC, SoD, audit trails
2. **Add Approval Workflows** - Multi-step approval for critical operations
3. **Implement Data Retention** - Automated archival and retention policies
4. **Compliance Automation** - Automatic alerts and enforcement
5. **Security Hardening** - Fix SQL injection, add CSRF protection, hash passwords
6. **Integration** - Connect to real maritime compliance systems

## ⚠️ Important Notes

- **DO NOT use in production** - This contains intentional vulnerabilities
- **Educational purposes only** - For training and demonstration
- **No real data** - All data is fictional
- **Not for public deployment** - Keep on local/internal networks only

## 📚 Additional Resources

- See `GOVERNANCE_ISSUES.md` for detailed documentation of all issues
- See `GITHUB_SETUP.md` for instructions on connecting to GitHub
- Maritime regulations: IMO, SOLAS, MARPOL, MLC, ISPS

## 📞 Support

This is a demonstration project for XT Group. For questions or issues, contact your project administrator.

---

**© 2025 XT Group - A legacy of excellence since 1956**  
*Service • Safety • Efficiency*