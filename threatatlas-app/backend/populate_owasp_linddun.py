"""
Populate knowledge base with OWASP Top 10 and LINDDUN frameworks.
Run this script to add web security and privacy threat modeling data.
"""
from app.database import SessionLocal
from app.models import Framework, Threat, Mitigation

# OWASP Top 10 (2021) Threats
OWASP_THREATS = [
    # A01:2021 - Broken Access Control
    {
        "name": "Insecure Direct Object References (IDOR)",
        "description": "Application exposes references to internal objects allowing attackers to access unauthorized data by modifying parameters",
        "category": "Broken Access Control"
    },
    {
        "name": "Path Traversal Attack",
        "description": "Attacker accesses files and directories outside the web root by manipulating file path variables",
        "category": "Broken Access Control"
    },
    {
        "name": "Missing Function Level Access Control",
        "description": "Application doesn't properly verify user permissions for administrative or privileged functions",
        "category": "Broken Access Control"
    },
    {
        "name": "Privilege Escalation",
        "description": "User gains elevated privileges beyond their authorization level through exploitation of access control flaws",
        "category": "Broken Access Control"
    },
    {
        "name": "Forced Browsing",
        "description": "Attacker accesses restricted pages or resources by directly requesting URLs without proper authorization checks",
        "category": "Broken Access Control"
    },

    # A02:2021 - Cryptographic Failures
    {
        "name": "Weak Encryption Algorithm Usage",
        "description": "Application uses outdated or weak cryptographic algorithms (MD5, SHA1, DES) that can be easily broken",
        "category": "Cryptographic Failures"
    },
    {
        "name": "Hardcoded Cryptographic Keys",
        "description": "Encryption keys are embedded in source code or configuration files, making them easily discoverable",
        "category": "Cryptographic Failures"
    },
    {
        "name": "Transmission of Sensitive Data in Cleartext",
        "description": "Passwords, credit cards, or personal data transmitted without encryption over HTTP or unencrypted channels",
        "category": "Cryptographic Failures"
    },
    {
        "name": "Insufficient SSL/TLS Configuration",
        "description": "Weak TLS versions (1.0/1.1) or cipher suites enabled, allowing downgrade attacks",
        "category": "Cryptographic Failures"
    },
    {
        "name": "Missing Certificate Validation",
        "description": "Application doesn't properly validate SSL/TLS certificates, enabling man-in-the-middle attacks",
        "category": "Cryptographic Failures"
    },

    # A03:2021 - Injection
    {
        "name": "SQL Injection",
        "description": "Attacker injects malicious SQL commands through user input to manipulate database queries and access unauthorized data",
        "category": "Injection"
    },
    {
        "name": "NoSQL Injection",
        "description": "Malicious queries injected into NoSQL databases (MongoDB, CouchDB) through unvalidated user input",
        "category": "Injection"
    },
    {
        "name": "OS Command Injection",
        "description": "Attacker executes arbitrary system commands on the server by injecting shell commands through application inputs",
        "category": "Injection"
    },
    {
        "name": "LDAP Injection",
        "description": "Malicious LDAP statements injected to manipulate directory service queries and bypass authentication",
        "category": "Injection"
    },
    {
        "name": "XML External Entity (XXE) Injection",
        "description": "Attacker injects malicious XML entities to access local files, perform SSRF, or cause denial of service",
        "category": "Injection"
    },

    # A04:2021 - Insecure Design
    {
        "name": "Missing Rate Limiting",
        "description": "Application lacks throttling mechanisms allowing brute force attacks and resource exhaustion",
        "category": "Insecure Design"
    },
    {
        "name": "Trust Boundary Violation",
        "description": "Application doesn't properly validate data crossing trust boundaries between components",
        "category": "Insecure Design"
    },
    {
        "name": "Insufficient Workflow Validation",
        "description": "Business logic flaws allow users to skip steps or manipulate multi-step processes",
        "category": "Insecure Design"
    },
    {
        "name": "Missing Security Requirements",
        "description": "Security controls not defined during design phase leading to fundamental architecture vulnerabilities",
        "category": "Insecure Design"
    },

    # A05:2021 - Security Misconfiguration
    {
        "name": "Default Credentials in Production",
        "description": "Default usernames and passwords not changed on production systems allowing easy unauthorized access",
        "category": "Security Misconfiguration"
    },
    {
        "name": "Unnecessary Features Enabled",
        "description": "Unused services, pages, accounts, or privileges enabled increasing attack surface",
        "category": "Security Misconfiguration"
    },
    {
        "name": "Directory Listing Enabled",
        "description": "Web server configured to show directory contents exposing sensitive files and application structure",
        "category": "Security Misconfiguration"
    },
    {
        "name": "Verbose Error Messages",
        "description": "Detailed error messages expose stack traces, database queries, or system information to attackers",
        "category": "Security Misconfiguration"
    },
    {
        "name": "Missing Security Headers",
        "description": "HTTP security headers (CSP, X-Frame-Options, HSTS) not configured leaving application vulnerable to attacks",
        "category": "Security Misconfiguration"
    },

    # A06:2021 - Vulnerable and Outdated Components
    {
        "name": "Use of Components with Known Vulnerabilities",
        "description": "Application uses outdated libraries, frameworks, or dependencies with publicly known security flaws",
        "category": "Vulnerable Components"
    },
    {
        "name": "Lack of Dependency Scanning",
        "description": "No automated scanning for vulnerable dependencies allowing outdated components to remain undetected",
        "category": "Vulnerable Components"
    },
    {
        "name": "Unpatched Software",
        "description": "Operating system, web server, or application server not regularly updated with security patches",
        "category": "Vulnerable Components"
    },

    # A07:2021 - Identification and Authentication Failures
    {
        "name": "Weak Password Policy",
        "description": "Application allows weak passwords without complexity requirements enabling brute force attacks",
        "category": "Authentication Failures"
    },
    {
        "name": "Missing Multi-Factor Authentication",
        "description": "Critical functions accessible with only password authentication making accounts vulnerable to credential theft",
        "category": "Authentication Failures"
    },
    {
        "name": "Session Fixation",
        "description": "Application doesn't regenerate session IDs after login allowing attackers to hijack authenticated sessions",
        "category": "Authentication Failures"
    },
    {
        "name": "Credential Stuffing Vulnerability",
        "description": "No protection against automated credential stuffing attacks using leaked password databases",
        "category": "Authentication Failures"
    },
    {
        "name": "Insecure Password Recovery",
        "description": "Password reset mechanism uses predictable tokens or security questions allowing account takeover",
        "category": "Authentication Failures"
    },

    # A08:2021 - Software and Data Integrity Failures
    {
        "name": "Insecure Deserialization",
        "description": "Application deserializes untrusted data allowing remote code execution or privilege escalation",
        "category": "Integrity Failures"
    },
    {
        "name": "Missing Code Signing",
        "description": "Software updates not digitally signed allowing malicious code injection through compromised update mechanisms",
        "category": "Integrity Failures"
    },
    {
        "name": "CI/CD Pipeline Compromise",
        "description": "Insecure build pipeline allows attackers to inject malicious code during development or deployment",
        "category": "Integrity Failures"
    },
    {
        "name": "Lack of Integrity Verification",
        "description": "Application doesn't verify integrity of critical data or code allowing tampering to go undetected",
        "category": "Integrity Failures"
    },

    # A09:2021 - Security Logging and Monitoring Failures
    {
        "name": "Insufficient Logging",
        "description": "Security events (failed logins, access violations) not logged preventing detection of attacks",
        "category": "Logging Failures"
    },
    {
        "name": "Log Injection",
        "description": "User input logged without sanitization allowing attackers to forge log entries or inject malicious content",
        "category": "Logging Failures"
    },
    {
        "name": "Missing Alerting for Critical Events",
        "description": "No real-time alerts for suspicious activities delaying incident response",
        "category": "Logging Failures"
    },
    {
        "name": "Logs Stored Insecurely",
        "description": "Log files accessible to unauthorized users or stored without encryption exposing sensitive data",
        "category": "Logging Failures"
    },

    # A10:2021 - Server-Side Request Forgery (SSRF)
    {
        "name": "Server-Side Request Forgery",
        "description": "Application fetches remote resources based on user input without validation, allowing access to internal systems",
        "category": "SSRF"
    },
    {
        "name": "Internal Service Exposure via SSRF",
        "description": "SSRF vulnerability allows scanning and accessing internal services not exposed to internet",
        "category": "SSRF"
    },
    {
        "name": "Cloud Metadata Service Abuse",
        "description": "SSRF used to access cloud metadata endpoints exposing credentials and configuration",
        "category": "SSRF"
    },
]

# OWASP Top 10 Mitigations
OWASP_MITIGATIONS = [
    # Broken Access Control
    {
        "name": "Implement Role-Based Access Control (RBAC)",
        "description": "Define user roles and enforce permissions at every access point with deny-by-default principle",
        "category": "Access Control"
    },
    {
        "name": "Use Indirect Object References",
        "description": "Map direct object references to user-specific session data preventing unauthorized access",
        "category": "Access Control"
    },
    {
        "name": "Enforce Access Control at API Layer",
        "description": "Verify authorization for every API endpoint and resource access preventing privilege escalation",
        "category": "Access Control"
    },

    # Cryptographic Failures
    {
        "name": "Use Strong Encryption Algorithms",
        "description": "Implement AES-256 for encryption and SHA-256 or better for hashing, avoid deprecated algorithms",
        "category": "Cryptography"
    },
    {
        "name": "Implement TLS 1.2+ with Strong Ciphers",
        "description": "Configure TLS 1.2 or 1.3 only with strong cipher suites, disable weak protocols",
        "category": "Cryptography"
    },
    {
        "name": "Use Key Management System (KMS)",
        "description": "Store encryption keys in dedicated KMS or hardware security modules, rotate regularly",
        "category": "Cryptography"
    },
    {
        "name": "Enforce HTTPS Everywhere",
        "description": "Redirect all HTTP traffic to HTTPS and implement HSTS header to prevent downgrade attacks",
        "category": "Cryptography"
    },

    # Injection
    {
        "name": "Use Parameterized Queries",
        "description": "Always use prepared statements with parameter binding for database queries preventing SQL injection",
        "category": "Input Validation"
    },
    {
        "name": "Input Validation and Sanitization",
        "description": "Validate all user input against whitelist patterns and sanitize before processing",
        "category": "Input Validation"
    },
    {
        "name": "Use ORM Frameworks Securely",
        "description": "Leverage ORM frameworks with parameterized queries, avoid raw SQL construction",
        "category": "Input Validation"
    },
    {
        "name": "Disable XML External Entity Processing",
        "description": "Configure XML parsers to disable external entity resolution preventing XXE attacks",
        "category": "Input Validation"
    },

    # Insecure Design
    {
        "name": "Implement Rate Limiting",
        "description": "Apply throttling on authentication, API endpoints, and resource-intensive operations",
        "category": "Secure Design"
    },
    {
        "name": "Use Threat Modeling",
        "description": "Conduct threat modeling during design phase to identify and address security risks early",
        "category": "Secure Design"
    },
    {
        "name": "Implement Defense in Depth",
        "description": "Layer multiple security controls so failure of one doesn't compromise entire system",
        "category": "Secure Design"
    },

    # Security Misconfiguration
    {
        "name": "Harden Default Configurations",
        "description": "Change all default credentials, disable unnecessary features, and follow security hardening guides",
        "category": "Configuration"
    },
    {
        "name": "Implement Security Headers",
        "description": "Configure CSP, X-Frame-Options, X-Content-Type-Options, HSTS, and other security headers",
        "category": "Configuration"
    },
    {
        "name": "Disable Directory Listing",
        "description": "Configure web server to prevent directory browsing and hide application structure",
        "category": "Configuration"
    },
    {
        "name": "Use Custom Error Pages",
        "description": "Display generic error messages to users while logging detailed errors securely",
        "category": "Configuration"
    },

    # Vulnerable Components
    {
        "name": "Implement Dependency Scanning",
        "description": "Use automated tools (Snyk, Dependabot) to scan and alert on vulnerable dependencies",
        "category": "Supply Chain"
    },
    {
        "name": "Establish Patch Management Process",
        "description": "Regularly update all components and have process for emergency patching of critical vulnerabilities",
        "category": "Supply Chain"
    },
    {
        "name": "Remove Unused Dependencies",
        "description": "Regularly audit and remove unused libraries and components reducing attack surface",
        "category": "Supply Chain"
    },

    # Authentication Failures
    {
        "name": "Implement Multi-Factor Authentication (MFA)",
        "description": "Require MFA for all users, especially for administrative and sensitive operations",
        "category": "Authentication"
    },
    {
        "name": "Enforce Strong Password Policy",
        "description": "Require minimum 12 characters, complexity requirements, and check against breached password databases",
        "category": "Authentication"
    },
    {
        "name": "Implement Account Lockout",
        "description": "Lock accounts after failed login attempts with exponential backoff to prevent brute force",
        "category": "Authentication"
    },
    {
        "name": "Regenerate Session IDs After Login",
        "description": "Create new session ID upon authentication to prevent session fixation attacks",
        "category": "Authentication"
    },

    # Integrity Failures
    {
        "name": "Implement Code Signing",
        "description": "Digitally sign all software releases and verify signatures before deployment",
        "category": "Integrity"
    },
    {
        "name": "Secure CI/CD Pipeline",
        "description": "Harden build servers, require code review, and scan for vulnerabilities in pipeline",
        "category": "Integrity"
    },
    {
        "name": "Avoid Unsafe Deserialization",
        "description": "Use safe serialization formats (JSON) and validate deserialized data against schema",
        "category": "Integrity"
    },

    # Logging Failures
    {
        "name": "Implement Comprehensive Logging",
        "description": "Log all security events including authentication, authorization failures, and input validation errors",
        "category": "Monitoring"
    },
    {
        "name": "Centralize Log Management",
        "description": "Send logs to centralized SIEM system for correlation and long-term retention",
        "category": "Monitoring"
    },
    {
        "name": "Implement Real-Time Alerting",
        "description": "Configure alerts for suspicious patterns like multiple failed logins or privilege escalation attempts",
        "category": "Monitoring"
    },

    # SSRF
    {
        "name": "Validate and Sanitize URLs",
        "description": "Whitelist allowed domains and protocols, validate URLs before making requests",
        "category": "Input Validation"
    },
    {
        "name": "Disable URL Redirects in Requests",
        "description": "Configure HTTP clients to not follow redirects automatically preventing SSRF bypass",
        "category": "Input Validation"
    },
    {
        "name": "Use Network Segmentation",
        "description": "Isolate application servers from internal networks and restrict outbound connections",
        "category": "Network Security"
    },
]

# LINDDUN Privacy Threats
LINDDUN_THREATS = [
    # Linkability
    {
        "name": "User Activity Tracking Across Sessions",
        "description": "Attacker correlates user activities across different sessions using persistent identifiers or browser fingerprinting",
        "category": "Linkability"
    },
    {
        "name": "Cross-Site Tracking via Third-Party Cookies",
        "description": "Third-party cookies and trackers link user behavior across multiple websites creating detailed profiles",
        "category": "Linkability"
    },
    {
        "name": "Location Data Correlation",
        "description": "GPS, IP address, or Wi-Fi data linked across time to track user movements and patterns",
        "category": "Linkability"
    },
    {
        "name": "Device Fingerprinting",
        "description": "Browser and device characteristics collected to create unique fingerprint enabling cross-session tracking",
        "category": "Linkability"
    },

    # Identifiability
    {
        "name": "Username Enumeration",
        "description": "Application reveals whether usernames or email addresses exist through different error messages or timing attacks",
        "category": "Identifiability"
    },
    {
        "name": "PII Exposure in URLs",
        "description": "Personally identifiable information included in URLs visible in browser history, logs, and referrer headers",
        "category": "Identifiability"
    },
    {
        "name": "Metadata Exposure in Files",
        "description": "Uploaded files contain metadata (author, location, device info) revealing user identity",
        "category": "Identifiability"
    },
    {
        "name": "Re-identification via Data Aggregation",
        "description": "Combining supposedly anonymous data points allows identification of individuals",
        "category": "Identifiability"
    },

    # Non-repudiation
    {
        "name": "Insufficient Audit Logging",
        "description": "User actions not properly logged allowing users to deny performing sensitive operations",
        "category": "Non-repudiation"
    },
    {
        "name": "Missing Digital Signatures",
        "description": "Transactions lack cryptographic signatures allowing users to claim they didn't authorize actions",
        "category": "Non-repudiation"
    },
    {
        "name": "Shared Account Usage",
        "description": "Multiple users sharing single account preventing attribution of specific actions to individuals",
        "category": "Non-repudiation"
    },

    # Detectability
    {
        "name": "Social Media Presence Linkage",
        "description": "User profiles linkable to social media accounts revealing additional personal information",
        "category": "Detectability"
    },
    {
        "name": "Public Data Aggregation",
        "description": "Publicly accessible user data aggregated to build comprehensive profiles without consent",
        "category": "Detectability"
    },
    {
        "name": "Pattern Analysis Revealing Behavior",
        "description": "Analysis of usage patterns reveals sensitive information about user behavior and preferences",
        "category": "Detectability"
    },

    # Disclosure of Information
    {
        "name": "Insufficient Data Anonymization",
        "description": "Personal data not properly anonymized before sharing with third parties or for analytics",
        "category": "Disclosure"
    },
    {
        "name": "Excessive Data Collection",
        "description": "Application collects more personal data than necessary for stated purposes",
        "category": "Disclosure"
    },
    {
        "name": "Insecure Data Sharing with Third Parties",
        "description": "Personal data shared with partners or vendors without proper security controls or user consent",
        "category": "Disclosure"
    },
    {
        "name": "Data Breach via Database Exposure",
        "description": "Personal data exposed through database vulnerabilities or misconfigurations",
        "category": "Disclosure"
    },
    {
        "name": "Sensitive Data in Client-Side Code",
        "description": "Personal or sensitive information embedded in JavaScript or HTML accessible to anyone",
        "category": "Disclosure"
    },

    # Unawareness (Content Unawareness)
    {
        "name": "Unclear Privacy Policy",
        "description": "Privacy policy written in complex legal language preventing users from understanding data practices",
        "category": "Unawareness"
    },
    {
        "name": "Hidden Data Collection",
        "description": "Application collects data without informing users or obtaining consent",
        "category": "Unawareness"
    },
    {
        "name": "Lack of Data Access Controls",
        "description": "Users cannot view, export, or delete their personal data as required by privacy regulations",
        "category": "Unawareness"
    },
    {
        "name": "Missing Privacy-Enhancing Features",
        "description": "No options for users to limit data collection or control privacy settings",
        "category": "Unawareness"
    },

    # Non-compliance
    {
        "name": "GDPR Violation - Missing Legal Basis",
        "description": "Personal data processed without valid legal basis (consent, contract, legitimate interest)",
        "category": "Non-compliance"
    },
    {
        "name": "GDPR Violation - Data Retention",
        "description": "Personal data retained longer than necessary violating data minimization principle",
        "category": "Non-compliance"
    },
    {
        "name": "CCPA Violation - Consumer Rights",
        "description": "Application doesn't provide required mechanisms for users to exercise CCPA rights",
        "category": "Non-compliance"
    },
    {
        "name": "Missing Data Protection Impact Assessment",
        "description": "High-risk processing activities conducted without required DPIA under GDPR",
        "category": "Non-compliance"
    },
    {
        "name": "International Data Transfer Violation",
        "description": "Personal data transferred internationally without adequate safeguards (SCCs, BCRs)",
        "category": "Non-compliance"
    },
]

# LINDDUN Mitigations
LINDDUN_MITIGATIONS = [
    # Linkability
    {
        "name": "Implement Cookie Consent Management",
        "description": "Use consent management platform to control tracking cookies and respect user privacy choices",
        "category": "Privacy Controls"
    },
    {
        "name": "Rotate Session Identifiers",
        "description": "Regularly rotate session IDs and use short-lived tokens to prevent long-term tracking",
        "category": "Privacy Controls"
    },
    {
        "name": "Block Third-Party Trackers",
        "description": "Implement Content Security Policy to block third-party tracking scripts and analytics",
        "category": "Privacy Controls"
    },
    {
        "name": "Minimize Browser Fingerprinting",
        "description": "Reduce uniqueness of browser characteristics and randomize canvas fingerprints",
        "category": "Privacy Controls"
    },

    # Identifiability
    {
        "name": "Use Generic Error Messages",
        "description": "Return same error message for all authentication failures preventing username enumeration",
        "category": "Data Protection"
    },
    {
        "name": "Strip Metadata from Files",
        "description": "Remove EXIF and metadata from user-uploaded files before storage or display",
        "category": "Data Protection"
    },
    {
        "name": "Implement k-Anonymity",
        "description": "Ensure data releases maintain k-anonymity preventing re-identification of individuals",
        "category": "Data Protection"
    },
    {
        "name": "Use Pseudonymization",
        "description": "Replace direct identifiers with pseudonyms making data attribution impossible without additional information",
        "category": "Data Protection"
    },

    # Non-repudiation
    {
        "name": "Implement Comprehensive Audit Trails",
        "description": "Log all user actions with timestamps and digital signatures for accountability",
        "category": "Accountability"
    },
    {
        "name": "Use Digital Signatures for Transactions",
        "description": "Require cryptographic signatures for sensitive operations providing proof of authorization",
        "category": "Accountability"
    },
    {
        "name": "Enforce Individual User Accounts",
        "description": "Prohibit account sharing and require unique credentials for each user",
        "category": "Accountability"
    },

    # Detectability
    {
        "name": "Implement Access Controls on Profiles",
        "description": "Allow users to control visibility of profile information and limit public data exposure",
        "category": "Privacy Controls"
    },
    {
        "name": "Provide Privacy Settings Dashboard",
        "description": "Give users granular control over what data is public, shared, or private",
        "category": "Privacy Controls"
    },
    {
        "name": "Use Differential Privacy",
        "description": "Add statistical noise to aggregated data preventing individual pattern detection",
        "category": "Data Protection"
    },

    # Disclosure
    {
        "name": "Implement Data Minimization",
        "description": "Collect only data essential for stated purposes and delete when no longer needed",
        "category": "Data Protection"
    },
    {
        "name": "Encrypt Personal Data at Rest",
        "description": "Use AES-256 encryption for all stored personal data with proper key management",
        "category": "Data Protection"
    },
    {
        "name": "Use Data Processing Agreements",
        "description": "Establish formal DPAs with all data processors ensuring GDPR compliance",
        "category": "Compliance"
    },
    {
        "name": "Implement Purpose Limitation",
        "description": "Use data only for explicitly stated purposes and obtain new consent for new uses",
        "category": "Compliance"
    },

    # Unawareness
    {
        "name": "Provide Clear Privacy Notices",
        "description": "Write privacy policy in plain language explaining data collection, use, and rights",
        "category": "Transparency"
    },
    {
        "name": "Implement Just-in-Time Notices",
        "description": "Show privacy notices at point of data collection explaining why data is needed",
        "category": "Transparency"
    },
    {
        "name": "Build User Data Dashboard",
        "description": "Allow users to view all collected data, download it, and request deletion",
        "category": "Transparency"
    },
    {
        "name": "Provide Privacy-Enhancing Settings",
        "description": "Offer privacy modes, anonymous browsing, and data collection opt-outs",
        "category": "Privacy Controls"
    },

    # Non-compliance
    {
        "name": "Conduct Data Protection Impact Assessment",
        "description": "Perform DPIA for high-risk processing activities as required by GDPR Article 35",
        "category": "Compliance"
    },
    {
        "name": "Implement Standard Contractual Clauses",
        "description": "Use SCCs for international data transfers ensuring adequate data protection",
        "category": "Compliance"
    },
    {
        "name": "Establish Data Retention Policies",
        "description": "Define and enforce retention periods for different data types with automated deletion",
        "category": "Compliance"
    },
    {
        "name": "Appoint Data Protection Officer",
        "description": "Designate DPO responsible for GDPR compliance and data protection strategy",
        "category": "Compliance"
    },
    {
        "name": "Implement Consent Management",
        "description": "Build system to obtain, record, and respect user consent for data processing",
        "category": "Compliance"
    },
]


def populate_knowledge_base():
    """Populate database with OWASP Top 10 and LINDDUN frameworks."""
    db = SessionLocal()

    try:
        print("Starting knowledge base population...")

        # Get or create OWASP Top 10 framework
        owasp_framework = db.query(Framework).filter(Framework.name == "OWASP Top 10").first()
        if not owasp_framework:
            owasp_framework = Framework(
                name="OWASP Top 10",
                description="OWASP Top 10 Web Application Security Risks - industry standard for web security"
            )
            db.add(owasp_framework)
            db.commit()
            db.refresh(owasp_framework)
            print(f"✓ Created OWASP Top 10 framework (ID: {owasp_framework.id})")
        else:
            print(f"✓ OWASP Top 10 framework already exists (ID: {owasp_framework.id})")

        # Add OWASP threats
        existing_owasp_threats = db.query(Threat).filter(Threat.framework_id == owasp_framework.id).count()
        if existing_owasp_threats == 0:
            for threat_data in OWASP_THREATS:
                threat = Threat(
                    framework_id=owasp_framework.id,
                    **threat_data
                )
                db.add(threat)
            db.commit()
            print(f"✓ Added {len(OWASP_THREATS)} OWASP Top 10 threats")
        else:
            print(f"✓ OWASP Top 10 threats already exist ({existing_owasp_threats} threats)")

        # Add OWASP mitigations
        existing_owasp_mitigations = db.query(Mitigation).filter(Mitigation.framework_id == owasp_framework.id).count()
        if existing_owasp_mitigations == 0:
            for mitigation_data in OWASP_MITIGATIONS:
                mitigation = Mitigation(
                    framework_id=owasp_framework.id,
                    **mitigation_data
                )
                db.add(mitigation)
            db.commit()
            print(f"✓ Added {len(OWASP_MITIGATIONS)} OWASP Top 10 mitigations")
        else:
            print(f"✓ OWASP Top 10 mitigations already exist ({existing_owasp_mitigations} mitigations)")

        # Get or create LINDDUN framework
        linddun_framework = db.query(Framework).filter(Framework.name == "LINDDUN").first()
        if not linddun_framework:
            linddun_framework = Framework(
                name="LINDDUN",
                description="LINDDUN Privacy Threat Modeling - systematic approach to privacy engineering"
            )
            db.add(linddun_framework)
            db.commit()
            db.refresh(linddun_framework)
            print(f"✓ Created LINDDUN framework (ID: {linddun_framework.id})")
        else:
            print(f"✓ LINDDUN framework already exists (ID: {linddun_framework.id})")

        # Add LINDDUN threats
        existing_linddun_threats = db.query(Threat).filter(Threat.framework_id == linddun_framework.id).count()
        if existing_linddun_threats == 0:
            for threat_data in LINDDUN_THREATS:
                threat = Threat(
                    framework_id=linddun_framework.id,
                    **threat_data
                )
                db.add(threat)
            db.commit()
            print(f"✓ Added {len(LINDDUN_THREATS)} LINDDUN privacy threats")
        else:
            print(f"✓ LINDDUN threats already exist ({existing_linddun_threats} threats)")

        # Add LINDDUN mitigations
        existing_linddun_mitigations = db.query(Mitigation).filter(Mitigation.framework_id == linddun_framework.id).count()
        if existing_linddun_mitigations == 0:
            for mitigation_data in LINDDUN_MITIGATIONS:
                mitigation = Mitigation(
                    framework_id=linddun_framework.id,
                    **mitigation_data
                )
                db.add(mitigation)
            db.commit()
            print(f"✓ Added {len(LINDDUN_MITIGATIONS)} LINDDUN privacy mitigations")
        else:
            print(f"✓ LINDDUN mitigations already exist ({existing_linddun_mitigations} mitigations)")

        print("\n" + "="*60)
        print("Knowledge base population completed successfully!")
        print("="*60)
        print(f"\nSummary:")
        print(f"  OWASP Top 10: {len(OWASP_THREATS)} threats, {len(OWASP_MITIGATIONS)} mitigations")
        print(f"  LINDDUN: {len(LINDDUN_THREATS)} threats, {len(LINDDUN_MITIGATIONS)} mitigations")
        print(f"  Total: {len(OWASP_THREATS) + len(LINDDUN_THREATS)} threats, {len(OWASP_MITIGATIONS) + len(LINDDUN_MITIGATIONS)} mitigations")

    except Exception as e:
        print(f"Error populating knowledge base: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_knowledge_base()
