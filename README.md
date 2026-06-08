# XT Shipping Governance Demo

A demonstration application showcasing governance and security issues in maritime shipping management systems, built for XT Group.

## About XT Group

XT Group is a global holding group comprised of diverse, innovative and market-leading companies. At the heart of the Group is XT Shipping, an established leading international ship owner and manager. The Group operates with a vision to provide the highest standards of Service, Safety, and Efficiency.

## Project Overview

This repository contains two versions of a Flask-based shipping management system:

- **broken-version**: Contains intentional governance and security issues for demonstration
- **fixed-version**: Implements proper governance controls and security measures

## Quick Start

### Broken Version (Port 5000)
```bash
cd broken-version
./run.sh
```
Login: `admin` / `admin123`

### Fixed Version (Port 5001)
```bash
cd fixed-version
./run.sh
```
Login: `admin` / `0000`

## Features

- Fleet Management
- Crew Management
- Cargo Operations
- Financial Transactions
- Compliance Monitoring
- Audit Logging

## Issues Demonstrated

The broken version contains 13 intentional issues across governance and security domains:

### Governance Issues (Primary Focus)
1. No Role-Based Access Control (RBAC)
2. Missing Segregation of Duties
3. Mutable Audit Logs
4. No Approval Workflows
5. Missing Certificate Expiry Automation
6. No Working Hours Enforcement
7. Missing Cargo Compliance Checks
8. No Data Retention Policies
9. Missing Compliance Monitoring

### Security Issues (Secondary)
10. SQL Injection Vulnerabilities
11. Hardcoded Credentials
12. Plaintext Password Storage
13. Weak Session Management

See [DEMO_SHOWCASE.md](DEMO_SHOWCASE.md) for detailed documentation with visualizations.

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Security**: Bcrypt (fixed version)

## Requirements

- Python 3.8+
- pip
- Virtual environment support

## Repository Structure

```
xt-shipping-governance-demo/
├── broken-version/          # Version with intentional issues
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── database/
│   └── run.sh
├── fixed-version/           # Version with proper controls
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── database/
│   └── run.sh
├── DEMO_SHOWCASE.md         # Detailed issue documentation
└── README.md
```

## License

This is a demonstration project for XT Group.