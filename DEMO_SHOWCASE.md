# 🚢 XT Shipping Management System
## Governance & Compliance Demo

---

## 🎯 Maritime Domain Issues

### 1. Crew Working Hours Violations

**The Problem:**
Crew members working excessive hours beyond international maritime law limits, creating safety risks and legal violations.

**Maritime Context:**
The Maritime Labour Convention (MLC) strictly limits crew working hours to prevent fatigue-related accidents. Violations can result in vessel detention at ports and significant fines.

```mermaid
graph LR
    A[Crew Member] -->|Works| B[240 hours/month]
    B -->|Exceeds| C[Legal Limit: 200h]
    C -->|Results in| D[Fatigue Risk]
    C -->|Results in| E[Port Detention]
    C -->|Results in| F[Legal Penalties]
    
    style B fill:#ff6b6b
    style C fill:#51cf66
    style D fill:#ffd43b
    style E fill:#ffd43b
    style F fill:#ffd43b
```

**The Fix:**
```mermaid
graph TD
    A[Crew Assignment] --> B{Check Hours}
    B -->|< 180h| C[Approve Assignment]
    B -->|180-200h| D[Warning Alert]
    B -->|> 200h| E[Block Assignment]
    D --> F[Manager Review]
    E --> G[Mandatory Rest Period]
    
    style C fill:#51cf66
    style D fill:#ffd43b
    style E fill:#ff6b6b
```

---

### 2. Expired Maritime Certifications

**The Problem:**
Vessels and crew operating with expired safety certificates, insurance, or qualifications.

**Maritime Context:**
International maritime regulations (SOLAS, MARPOL) require valid certifications for all vessels and crew. Operating without valid certificates voids insurance and can result in vessel detention.

```mermaid
graph TB
    A[Vessel: XT Navigator] --> B[Insurance Expired]
    A --> C[Still Marked Active]
    C --> D[Carrying Cargo]
    D --> E[Unlimited Liability Risk]
    D --> F[Port Detention Risk]
    D --> G[Legal Violations]
    
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    style E fill:#ffd43b
    style F fill:#ffd43b
    style G fill:#ffd43b
```

**The Fix:**
```mermaid
graph LR
    A[Certificate Check] --> B{Days to Expiry}
    B -->|> 90 days| C[Active Status]
    B -->|30-90 days| D[Warning Alert]
    B -->|< 30 days| E[Critical Alert]
    B -->|Expired| F[Auto-Ground Vessel]
    F --> G[Block Operations]
    
    style C fill:#51cf66
    style D fill:#ffd43b
    style E fill:#ff9800
    style F fill:#ff6b6b
```

---

### 3. Cargo Compliance Violations

**The Problem:**
Hazardous cargo loaded without proper documentation or safety approvals.

**Maritime Context:**
International Maritime Dangerous Goods (IMDG) Code requires strict documentation and approval for hazardous materials. Violations can cause environmental disasters and criminal liability.

```mermaid
sequenceDiagram
    participant User
    participant System
    participant Compliance
    
    User->>System: Create Cargo: Chemicals
    System->>System: Skip Safety Check
    System->>System: Skip Documentation
    System->>Compliance: No Compliance Review
    System->>User: Approved ✓
    
    Note over System,Compliance: Missing: IMDG Certificate
    Note over System,Compliance: Missing: Safety Data Sheet
    Note over System,Compliance: Missing: Port Authority Approval
```

**The Fix:**
```mermaid
sequenceDiagram
    participant User
    participant System
    participant Compliance
    participant Authority
    
    User->>System: Create Cargo: Chemicals
    System->>Compliance: Check IMDG Requirements
    Compliance->>System: Require Documentation
    System->>User: Request Safety Data Sheet
    User->>System: Upload Documents
    System->>Authority: Submit for Approval
    Authority->>System: Approved ✓
    System->>User: Cargo Approved
```

---

### 4. Missing Data Retention Policies

**The Problem:**
No automated data retention or archival policies for maritime records.

**Maritime Context:**
Maritime regulations require retention of voyage records, crew logs, and cargo manifests for 5-10 years for legal and insurance purposes.

```mermaid
graph TD
    A[Old Records] --> B[No Retention Policy]
    B --> C[Manual Deletion Possible]
    B --> D[No Archival Process]
    C --> E[Legal Evidence Lost]
    D --> F[Compliance Violations]
    
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    style D fill:#ff6b6b
```

**The Fix:**
```mermaid
graph TD
    A[Record Created] --> B{Age Check}
    B -->|< 5 years| C[Active Storage]
    B -->|5-10 years| D[Archive Storage]
    B -->|> 10 years| E[Secure Deletion]
    D --> F[Read-Only Access]
    E --> G[Audit Trail]
    
    style C fill:#51cf66
    style D fill:#4dabf7
    style E fill:#ffd43b
```

---

## 🔐 Governance & Control Issues

### 5. Segregation of Duties Violation

**The Problem:**
Same person can create and approve their own financial transactions, enabling fraud.

```mermaid
graph TD
    A[User: John] -->|Creates| B[Transaction: $200,000]
    A -->|Approves| B
    B --> C[Payment Processed]
    
    style A fill:#ff6b6b
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    
    Note1[Same Person = Fraud Risk]
```

**The Fix:**
```mermaid
graph TD
    A[User: John] -->|Creates| B[Transaction: $200,000]
    B -->|Pending| C[Manager: Sarah]
    C -->|Reviews| D{Approve?}
    D -->|Yes| E[Payment Processed]
    D -->|No| F[Rejected]
    
    style A fill:#4dabf7
    style C fill:#51cf66
    style E fill:#51cf66
    style F fill:#ffd43b
```

---

### 6. Deletable Audit Logs

**The Problem:**
Users can delete their own audit trail, destroying evidence of actions.

```mermaid
graph LR
    A[User Action] --> B[Audit Log Created]
    B --> C[User Deletes Log]
    C --> D[Evidence Lost]
    
    style C fill:#ff6b6b
    style D fill:#ff6b6b
```

**The Fix:**
```mermaid
graph LR
    A[User Action] --> B[Audit Log Created]
    B --> C[Cryptographically Signed]
    C --> D[Append-Only Storage]
    D --> E[Immutable Record]
    
    style C fill:#51cf66
    style D fill:#51cf66
    style E fill:#51cf66
```

---

### 7. Missing Role-Based Access Control

**The Problem:**
All users can access all data regardless of their role or need.

```mermaid
graph TD
    A[All Users] --> B[Full System Access]
    B --> C[Financial Data]
    B --> D[Crew Records]
    B --> E[Compliance Reports]
    B --> F[Executive Data]
    
    style A fill:#ff6b6b
    style B fill:#ff6b6b
```

**The Fix:**
```mermaid
graph TD
    A[User Login] --> B{Role Check}
    B -->|Clerk| C[Basic Operations]
    B -->|Manager| D[Department Data]
    B -->|Executive| E[All Data]
    B -->|Captain| F[Vessel Operations]
    
    style B fill:#4dabf7
    style C fill:#51cf66
    style D fill:#51cf66
    style E fill:#51cf66
    style F fill:#51cf66
```

---

### 8. No Approval Workflows

**The Problem:**
Critical operations execute immediately without review or approval process.

```mermaid
graph LR
    A[User Request] --> B[Immediate Execution]
    B --> C[No Review]
    B --> D[No Approval]
    
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    style D fill:#ff6b6b
```

**The Fix:**
```mermaid
graph TD
    A[User Request] --> B[Pending State]
    B --> C[Manager Review]
    C --> D{Decision}
    D -->|Approve| E[Execute]
    D -->|Reject| F[Cancel]
    D -->|Request Changes| G[Back to User]
    
    style B fill:#ffd43b
    style C fill:#4dabf7
    style E fill:#51cf66
```

---

### 9. Missing Compliance Monitoring

**The Problem:**
No automated system to monitor and enforce compliance with maritime regulations.

```mermaid
graph TD
    A[Operations] --> B[No Monitoring]
    B --> C[Manual Checks Only]
    C --> D[Violations Undetected]
    D --> E[Regulatory Fines]
    
    style B fill:#ff6b6b
    style C fill:#ff6b6b
    style D fill:#ff6b6b
```

**The Fix:**
```mermaid
graph TD
    A[Operations] --> B[Real-time Monitoring]
    B --> C{Compliance Check}
    C -->|Pass| D[Continue]
    C -->|Warning| E[Alert Manager]
    C -->|Fail| F[Block Operation]
    E --> G[Corrective Action]
    
    style B fill:#51cf66
    style C fill:#4dabf7
    style D fill:#51cf66
```

---

## 🔒 Security Vulnerabilities

### 10. SQL Injection

**The Problem:**
User input directly concatenated into SQL queries, allowing database manipulation.

```mermaid
graph LR
    A[User Input] -->|Unsanitized| B[SQL Query]
    B --> C[Database]
    C --> D[Data Breach]
    C --> E[Data Manipulation]
    
    style A fill:#ff6b6b
    style B fill:#ff6b6b
    style D fill:#ff6b6b
    style E fill:#ff6b6b
```

**Example Attack:**
```
Username: admin' OR '1'='1
Password: anything
Result: Bypass authentication
```

**The Fix:**
```mermaid
graph LR
    A[User Input] --> B[Input Validation]
    B --> C[Parameterized Query]
    C --> D[Database]
    D --> E[Safe Execution]
    
    style B fill:#51cf66
    style C fill:#51cf66
    style E fill:#51cf66
```

---

### 11. Hardcoded Credentials

**The Problem:**
Default admin credentials hardcoded in the database and visible in login page.

```mermaid
graph TD
    A[Source Code] --> B[Hardcoded Passwords]
    B --> C[admin/admin123]
    B --> D[captain/captain123]
    B --> E[finance/finance123]
    C --> F[Easy to Guess]
    D --> F
    E --> F
    F --> G[Unauthorized Access]
    
    style B fill:#ff6b6b
    style F fill:#ff6b6b
    style G fill:#ff6b6b
```

**The Fix:**
```mermaid
graph TD
    A[User Registration] --> B[Strong Password Policy]
    B --> C[Password Hashing]
    C --> D[Secure Storage]
    D --> E[Multi-Factor Auth]
    
    style B fill:#51cf66
    style C fill:#51cf66
    style D fill:#51cf66
    style E fill:#51cf66
```

---

### 12. Plaintext Password Storage

**The Problem:**
Passwords stored in database without encryption or hashing.

```mermaid
graph LR
    A[User Password] -->|No Encryption| B[Database]
    B --> C[Plaintext Storage]
    C --> D[Database Breach]
    D --> E[All Passwords Exposed]
    
    style A fill:#ff6b6b
    style C fill:#ff6b6b
    style E fill:#ff6b6b
```

**The Fix:**
```mermaid
graph LR
    A[User Password] --> B[Salt Generation]
    B --> C[Bcrypt Hashing]
    C --> D[Hashed Storage]
    D --> E[Secure Verification]
    
    style B fill:#51cf66
    style C fill:#51cf66
    style D fill:#51cf66
    style E fill:#51cf66
```

---

### 13. Insecure Session Management

**The Problem:**
Session data stored in client-side cookies without encryption or validation.

```mermaid
graph TD
    A[User Login] --> B[Session Cookie]
    B --> C[No Encryption]
    B --> D[No Expiration]
    B --> E[No Validation]
    C --> F[Session Hijacking]
    D --> F
    E --> F
    
    style C fill:#ff6b6b
    style D fill:#ff6b6b
    style E fill:#ff6b6b
    style F fill:#ff6b6b
```

**The Fix:**
```mermaid
graph TD
    A[User Login] --> B[Secure Session]
    B --> C[Server-side Storage]
    B --> D[Encrypted Token]
    B --> E[Auto Expiration]
    B --> F[IP Validation]
    
    style C fill:#51cf66
    style D fill:#51cf66
    style E fill:#51cf66
    style F fill:#51cf66
```

---

## 🔧 Solution Roadmap

```mermaid
gantt
    title Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Critical Fixes
    Segregation of Duties           :crit, 2026-06-07, 7d
    Immutable Audit Logs           :crit, 2026-06-07, 7d
    SQL Injection Prevention       :crit, 2026-06-07, 5d
    Password Security              :crit, 2026-06-12, 5d
    
    section High Priority
    Certificate Expiry Automation  :2026-06-14, 7d
    Working Hours Enforcement      :2026-06-14, 7d
    Role-Based Access Control      :2026-06-21, 10d
    Cargo Compliance Automation    :2026-06-21, 10d
    
    section Medium Priority
    Approval Workflows            :2026-07-01, 7d
    Data Retention Policies       :2026-07-08, 14d
    Compliance Monitoring         :2026-07-08, 14d
    Session Security              :2026-07-15, 7d
```

---

## 📊 Impact Analysis

```mermaid
graph TD
    A[Current State] --> B[High Risk]
    B --> C[Fraud Exposure]
    B --> D[Legal Violations]
    B --> E[Safety Risks]
    B --> F[Security Breaches]
    
    G[After Fixes] --> H[Controlled Environment]
    H --> I[Fraud Prevention]
    H --> J[Regulatory Compliance]
    H --> K[Enhanced Safety]
    H --> L[Secure Operations]
    
    style A fill:#ff6b6b
    style B fill:#ff6b6b
    style G fill:#51cf66
    style H fill:#51cf66
```

---

## 🎬 Live Demo Walkthrough

### Step 1: Login & Security Issues
- Demonstrate SQL injection vulnerability
- Show hardcoded credentials on login page
- Display plaintext passwords in database

### Step 2: Access Control Problems
- Login as clerk and access executive financial data
- Show unrestricted access across all roles
- Demonstrate missing RBAC

### Step 3: Maritime Compliance Violations
- Display crew member with 240 working hours (exceeds 200h limit)
- Show expired maritime certificates still marked as "Active"
- View vessel with expired insurance carrying cargo

### Step 4: Governance Failures
- Create a $200,000 transaction
- Approve it with the same user account
- Highlight the segregation of duties violation

### Step 5: Audit Trail Manipulation
- View audit logs of previous actions
- Delete an audit log entry
- Show how evidence can be destroyed

### Step 6: Cargo & Compliance
- Create hazardous cargo without safety documentation
- Show missing IMDG compliance checks
- Demonstrate lack of approval workflows

### Step 7: Compliance Dashboard
- Review comprehensive list of all violations
- Show real-time compliance status
- Demonstrate the scope of governance gaps

---

## 💡 Business Value

### Risk Mitigation
- Prevents fraud through proper controls
- Eliminates unlimited liability exposure
- Ensures maritime safety compliance
- Protects against cyber attacks

### Operational Excellence
- Automated compliance monitoring
- Reduced manual oversight requirements
- Proactive risk management
- Streamlined approval processes

### Regulatory Compliance
- Meets international maritime standards (IMO, SOLAS, MLC)
- Satisfies financial regulations (SOX)
- Maintains audit trail integrity
- Ensures data protection (GDPR)

---

**XT Group** | *Service • Safety • Efficiency*