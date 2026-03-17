"""
Knowledge base seeder — auto-populates frameworks, threats, and mitigations.

Called automatically on application startup via the FastAPI lifespan hook.
Fully idempotent: safe to run multiple times; existing entries are never
modified or duplicated.

Adding a new framework
----------------------
Append a new dict to FRAMEWORKS_REGISTRY following this structure:

    {
        "name":        "My Framework",
        "description": "Short description shown in the UI.",
        "threats": [
            {"name": "...", "description": "...", "category": "..."},
        ],
        "mitigations": [
            {"name": "...", "description": "...", "category": "..."},
        ],
    },

Restart the application (or the Docker service) — seeding runs automatically.
"""

import logging

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Framework, Mitigation, Threat

logger = logging.getLogger(__name__)


# ── Framework registry ────────────────────────────────────────────────────────
# Each entry defines one framework.  Add new frameworks here.

FRAMEWORKS_REGISTRY = [
    # ── STRIDE ────────────────────────────────────────────────────────────────
    {
        "name": "STRIDE",
        "description": (
            "STRIDE Threat Modeling — Spoofing, Tampering, Repudiation, "
            "Information Disclosure, Denial of Service, Elevation of Privilege"
        ),
        "threats": [
            # Spoofing
            {"name": "Credential Theft via Phishing", "category": "Spoofing",
             "description": "Attacker sends phishing emails to steal user credentials by impersonating legitimate services"},
            {"name": "Session Hijacking", "category": "Spoofing",
             "description": "Attacker steals or predicts session tokens to impersonate authenticated users"},
            {"name": "Man-in-the-Middle Attack", "category": "Spoofing",
             "description": "Attacker intercepts communication between client and server to steal credentials or session data"},
            {"name": "IP Spoofing", "category": "Spoofing",
             "description": "Attacker forges source IP address to bypass IP-based authentication or hide identity"},
            {"name": "DNS Spoofing", "category": "Spoofing",
             "description": "Attacker corrupts DNS cache to redirect users to malicious websites"},
            # Tampering
            {"name": "SQL Injection", "category": "Tampering",
             "description": "Attacker injects malicious SQL code through user inputs to manipulate database queries"},
            {"name": "Cross-Site Scripting (XSS)", "category": "Tampering",
             "description": "Attacker injects malicious scripts into web pages viewed by other users"},
            {"name": "Parameter Tampering", "category": "Tampering",
             "description": "Attacker modifies URL parameters, form fields, or cookies to manipulate application behavior"},
            {"name": "Code Injection", "category": "Tampering",
             "description": "Attacker injects malicious code into application to execute arbitrary commands"},
            {"name": "File Upload Exploitation", "category": "Tampering",
             "description": "Attacker uploads malicious files to compromise server or execute code"},
            {"name": "Configuration File Manipulation", "category": "Tampering",
             "description": "Attacker modifies configuration files to alter application behavior or gain elevated privileges"},
            # Repudiation
            {"name": "Insufficient Audit Logging", "category": "Repudiation",
             "description": "Critical actions are not logged, allowing attackers to perform malicious activities without detection"},
            {"name": "Log Tampering", "category": "Repudiation",
             "description": "Attacker modifies or deletes audit logs to hide malicious activities"},
            {"name": "Transaction Denial", "category": "Repudiation",
             "description": "User denies performing a transaction due to lack of non-repudiation controls"},
            {"name": "Clock Manipulation", "category": "Repudiation",
             "description": "Attacker manipulates system time to falsify timestamps in logs and transactions"},
            # Information Disclosure
            {"name": "Sensitive Data Exposure in Logs", "category": "Information Disclosure",
             "description": "Application logs contain sensitive information like passwords, tokens, or PII"},
            {"name": "Directory Traversal", "category": "Information Disclosure",
             "description": "Attacker accesses files outside intended directory by manipulating file paths"},
            {"name": "Insecure Direct Object References", "category": "Information Disclosure",
             "description": "Application exposes internal object references allowing unauthorized access to data"},
            {"name": "Information Leakage via Error Messages", "category": "Information Disclosure",
             "description": "Detailed error messages reveal sensitive system information to attackers"},
            {"name": "Unencrypted Data Transmission", "category": "Information Disclosure",
             "description": "Sensitive data transmitted over network without encryption can be intercepted"},
            {"name": "Metadata Exposure", "category": "Information Disclosure",
             "description": "Application exposes sensitive metadata in HTTP headers, comments, or API responses"},
            {"name": "Memory Dump Exposure", "category": "Information Disclosure",
             "description": "Sensitive data in memory dumps can be accessed by unauthorized users"},
            # Denial of Service
            {"name": "Resource Exhaustion Attack", "category": "Denial of Service",
             "description": "Attacker consumes system resources (CPU, memory, disk) to make service unavailable"},
            {"name": "Application-Layer DDoS", "category": "Denial of Service",
             "description": "Attacker floods application with legitimate-looking requests to overwhelm servers"},
            {"name": "Regex Denial of Service (ReDoS)", "category": "Denial of Service",
             "description": "Attacker exploits inefficient regular expressions to cause catastrophic backtracking"},
            {"name": "Database Connection Pool Exhaustion", "category": "Denial of Service",
             "description": "Attacker opens many database connections until pool is exhausted"},
            {"name": "XML Bomb (Billion Laughs)", "category": "Denial of Service",
             "description": "Attacker sends malicious XML with recursive entity expansion to exhaust memory"},
            {"name": "Slowloris Attack", "category": "Denial of Service",
             "description": "Attacker sends partial HTTP requests slowly to keep connections open and exhaust server"},
            # Elevation of Privilege
            {"name": "Privilege Escalation via IDOR", "category": "Elevation of Privilege",
             "description": "Attacker manipulates object references to access resources belonging to higher-privileged users"},
            {"name": "Authentication Bypass", "category": "Elevation of Privilege",
             "description": "Attacker circumvents authentication mechanisms to gain unauthorized access"},
            {"name": "Authorization Bypass", "category": "Elevation of Privilege",
             "description": "Attacker bypasses authorization checks to access restricted functionality"},
            {"name": "Cross-Site Request Forgery (CSRF)", "category": "Elevation of Privilege",
             "description": "Attacker tricks authenticated user into performing unwanted actions"},
            {"name": "Insecure Deserialization", "category": "Elevation of Privilege",
             "description": "Attacker exploits deserialization to execute arbitrary code or escalate privileges"},
            {"name": "JWT Token Manipulation", "category": "Elevation of Privilege",
             "description": "Attacker modifies JWT claims to escalate privileges or impersonate users"},
        ],
        "mitigations": [
            # Spoofing
            {"name": "Multi-Factor Authentication (MFA)", "category": "Spoofing",
             "description": "Implement MFA requiring multiple verification factors (password, OTP, biometrics) to prevent credential theft"},
            {"name": "Certificate-Based Authentication", "category": "Spoofing",
             "description": "Use digital certificates for mutual TLS authentication to verify identity of both parties"},
            {"name": "Secure Session Management", "category": "Spoofing",
             "description": "Implement secure session tokens with proper expiration, rotation, and HTTPOnly/Secure flags"},
            {"name": "TLS/SSL Encryption", "category": "Spoofing",
             "description": "Enforce HTTPS with TLS 1.2+ to protect against man-in-the-middle attacks"},
            {"name": "DNSSEC Implementation", "category": "Spoofing",
             "description": "Use DNSSEC to authenticate DNS responses and prevent DNS spoofing"},
            # Tampering
            {"name": "Input Validation and Sanitization", "category": "Tampering",
             "description": "Validate and sanitize all user inputs using allowlists and proper encoding"},
            {"name": "Parameterized Queries", "category": "Tampering",
             "description": "Use prepared statements with parameterized queries to prevent SQL injection"},
            {"name": "Content Security Policy (CSP)", "category": "Tampering",
             "description": "Implement CSP headers to prevent XSS attacks by controlling resource loading"},
            {"name": "Digital Signatures", "category": "Tampering",
             "description": "Use cryptographic signatures to verify data integrity and detect tampering"},
            {"name": "File Upload Restrictions", "category": "Tampering",
             "description": "Implement file type validation, size limits, and virus scanning for uploads"},
            {"name": "Code Signing", "category": "Tampering",
             "description": "Sign application code and verify signatures to prevent code injection"},
            # Repudiation
            {"name": "Comprehensive Audit Logging", "category": "Repudiation",
             "description": "Log all critical operations with timestamps, user identity, and action details"},
            {"name": "Tamper-Proof Log Storage", "category": "Repudiation",
             "description": "Store logs in append-only systems or use blockchain for immutable audit trails"},
            {"name": "Digital Transaction Signatures", "category": "Repudiation",
             "description": "Require cryptographic signatures for critical transactions to ensure non-repudiation"},
            {"name": "Secure Time Synchronization", "category": "Repudiation",
             "description": "Use NTP with authentication to maintain accurate timestamps across systems"},
            {"name": "Log Integrity Monitoring", "category": "Repudiation",
             "description": "Implement SIEM solutions to detect log tampering and unauthorized modifications"},
            # Information Disclosure
            {"name": "Data Encryption at Rest", "category": "Information Disclosure",
             "description": "Encrypt sensitive data stored in databases and file systems using AES-256"},
            {"name": "Data Encryption in Transit", "category": "Information Disclosure",
             "description": "Use TLS/SSL for all data transmission to prevent interception"},
            {"name": "Access Control Lists (ACLs)", "category": "Information Disclosure",
             "description": "Implement fine-grained access controls to restrict data access based on user roles"},
            {"name": "Secure Error Handling", "category": "Information Disclosure",
             "description": "Implement generic error messages for users while logging detailed errors securely"},
            {"name": "Data Masking and Redaction", "category": "Information Disclosure",
             "description": "Mask sensitive data in logs, UI, and API responses to prevent exposure"},
            {"name": "Security Headers", "category": "Information Disclosure",
             "description": "Implement security headers (X-Content-Type-Options, X-Frame-Options, etc.) to prevent information leakage"},
            # Denial of Service
            {"name": "Rate Limiting", "category": "Denial of Service",
             "description": "Implement rate limiting per user/IP to prevent resource exhaustion attacks"},
            {"name": "Web Application Firewall (WAF)", "category": "Denial of Service",
             "description": "Deploy WAF to filter malicious traffic and protect against application-layer attacks"},
            {"name": "Connection Pooling", "category": "Denial of Service",
             "description": "Implement connection pools with proper limits and timeouts to prevent exhaustion"},
            {"name": "Input Size Limits", "category": "Denial of Service",
             "description": "Enforce maximum size limits on requests, uploads, and XML/JSON payloads"},
            {"name": "Auto-Scaling", "category": "Denial of Service",
             "description": "Implement auto-scaling to handle traffic spikes and distribute load"},
            {"name": "Request Timeout Configuration", "category": "Denial of Service",
             "description": "Set appropriate timeouts for connections and requests to prevent slowloris attacks"},
            # Elevation of Privilege
            {"name": "Role-Based Access Control (RBAC)", "category": "Elevation of Privilege",
             "description": "Implement RBAC to ensure users only access resources appropriate for their role"},
            {"name": "Principle of Least Privilege", "category": "Elevation of Privilege",
             "description": "Grant minimum necessary permissions to users and services"},
            {"name": "Authorization Checks", "category": "Elevation of Privilege",
             "description": "Verify user permissions for every protected resource and action"},
            {"name": "CSRF Tokens", "category": "Elevation of Privilege",
             "description": "Implement anti-CSRF tokens for all state-changing operations"},
            {"name": "JWT Signature Verification", "category": "Elevation of Privilege",
             "description": "Verify JWT signatures and validate claims before trusting token data"},
            {"name": "Secure Deserialization", "category": "Elevation of Privilege",
             "description": "Avoid deserializing untrusted data or use safe serialization formats like JSON"},
        ],
    },

    # ── PASTA ─────────────────────────────────────────────────────────────────
    {
        "name": "PASTA",
        "description": (
            "Process for Attack Simulation and Threat Analysis — "
            "a risk-centric threat modeling methodology"
        ),
        "threats": [
            {"name": "API Key Exposure in Client-Side Code", "category": "Asset Analysis",
             "description": "API keys or secrets hardcoded in frontend code can be extracted by attackers"},
            {"name": "Insufficient API Authentication", "category": "Attack Surface Analysis",
             "description": "API endpoints lack proper authentication allowing unauthorized access"},
            {"name": "Mass Assignment Vulnerability", "category": "Attack Modeling",
             "description": "API allows modification of object properties that should be restricted"},
            {"name": "Broken Object Level Authorization", "category": "Threat Analysis",
             "description": "API fails to validate user ownership of resources before allowing access"},
            {"name": "Excessive Data Exposure", "category": "Vulnerability Analysis",
             "description": "API returns more data than necessary, exposing sensitive information"},
            {"name": "Lack of Rate Limiting on Sensitive Operations", "category": "Attack Modeling",
             "description": "No rate limiting on password reset, account creation, or financial transactions"},
            {"name": "Insecure Direct Object References in APIs", "category": "Threat Analysis",
             "description": "Predictable resource IDs allow enumeration and unauthorized access"},
            {"name": "GraphQL Query Depth Attack", "category": "Attack Surface Analysis",
             "description": "Deeply nested GraphQL queries exhaust server resources"},
            {"name": "WebSocket Connection Hijacking", "category": "Attack Modeling",
             "description": "Unprotected WebSocket connections allow message interception or injection"},
            {"name": "Server-Side Request Forgery (SSRF)", "category": "Threat Analysis",
             "description": "Attacker tricks server into making requests to internal systems"},
        ],
        "mitigations": [
            {"name": "Environment Variable Management", "category": "Asset Analysis",
             "description": "Store secrets in environment variables or secret management systems, never in code"},
            {"name": "API Gateway with Authentication", "category": "Attack Surface Analysis",
             "description": "Implement API gateway with OAuth2/JWT authentication for all endpoints"},
            {"name": "DTO Validation and Whitelisting", "category": "Attack Modeling",
             "description": "Use Data Transfer Objects with explicit property whitelisting to prevent mass assignment"},
            {"name": "Object-Level Authorization Checks", "category": "Threat Analysis",
             "description": "Verify user ownership before allowing access to any resource"},
            {"name": "Response Filtering", "category": "Vulnerability Analysis",
             "description": "Filter API responses to return only necessary fields using DTOs or GraphQL field selection"},
            {"name": "Distributed Rate Limiting", "category": "Attack Modeling",
             "description": "Implement Redis-based distributed rate limiting across all API instances"},
            {"name": "UUID-Based Resource Identifiers", "category": "Threat Analysis",
             "description": "Use UUIDs instead of sequential IDs to prevent enumeration attacks"},
            {"name": "GraphQL Query Complexity Analysis", "category": "Attack Surface Analysis",
             "description": "Implement query depth and complexity limits for GraphQL endpoints"},
            {"name": "WebSocket Authentication and Validation", "category": "Attack Modeling",
             "description": "Authenticate WebSocket connections and validate all messages"},
            {"name": "SSRF Protection with URL Validation", "category": "Threat Analysis",
             "description": "Validate and whitelist allowed URLs, disable URL redirects, and use internal DNS filtering"},
        ],
    },

    # ── OWASP Top 10 ──────────────────────────────────────────────────────────
    {
        "name": "OWASP Top 10",
        "description": (
            "OWASP Top 10 Web Application Security Risks — "
            "industry standard awareness document for web application security"
        ),
        "threats": [
            # A01 — Broken Access Control
            {"name": "Insecure Direct Object References (IDOR)", "category": "Broken Access Control",
             "description": "Application exposes references to internal objects allowing attackers to access unauthorized data by modifying parameters"},
            {"name": "Path Traversal Attack", "category": "Broken Access Control",
             "description": "Attacker accesses files and directories outside the web root by manipulating file path variables"},
            {"name": "Missing Function Level Access Control", "category": "Broken Access Control",
             "description": "Application doesn't properly verify user permissions for administrative or privileged functions"},
            {"name": "Privilege Escalation", "category": "Broken Access Control",
             "description": "User gains elevated privileges beyond their authorization level through exploitation of access control flaws"},
            {"name": "Forced Browsing", "category": "Broken Access Control",
             "description": "Attacker accesses restricted pages or resources by directly requesting URLs without proper authorization checks"},
            # A02 — Cryptographic Failures
            {"name": "Weak Encryption Algorithm Usage", "category": "Cryptographic Failures",
             "description": "Application uses outdated or weak cryptographic algorithms (MD5, SHA1, DES) that can be easily broken"},
            {"name": "Hardcoded Cryptographic Keys", "category": "Cryptographic Failures",
             "description": "Encryption keys are embedded in source code or configuration files, making them easily discoverable"},
            {"name": "Transmission of Sensitive Data in Cleartext", "category": "Cryptographic Failures",
             "description": "Passwords, credit cards, or personal data transmitted without encryption over HTTP or unencrypted channels"},
            {"name": "Insufficient SSL/TLS Configuration", "category": "Cryptographic Failures",
             "description": "Weak TLS versions (1.0/1.1) or cipher suites enabled, allowing downgrade attacks"},
            {"name": "Missing Certificate Validation", "category": "Cryptographic Failures",
             "description": "Application doesn't properly validate SSL/TLS certificates, enabling man-in-the-middle attacks"},
            # A03 — Injection
            {"name": "SQL Injection", "category": "Injection",
             "description": "Attacker injects malicious SQL commands through user input to manipulate database queries and access unauthorized data"},
            {"name": "NoSQL Injection", "category": "Injection",
             "description": "Malicious queries injected into NoSQL databases (MongoDB, CouchDB) through unvalidated user input"},
            {"name": "OS Command Injection", "category": "Injection",
             "description": "Attacker executes arbitrary system commands on the server by injecting shell commands through application inputs"},
            {"name": "LDAP Injection", "category": "Injection",
             "description": "Malicious LDAP statements injected to manipulate directory service queries and bypass authentication"},
            {"name": "XML External Entity (XXE) Injection", "category": "Injection",
             "description": "Attacker injects malicious XML entities to access local files, perform SSRF, or cause denial of service"},
            # A04 — Insecure Design
            {"name": "Missing Rate Limiting", "category": "Insecure Design",
             "description": "Application lacks throttling mechanisms allowing brute force attacks and resource exhaustion"},
            {"name": "Trust Boundary Violation", "category": "Insecure Design",
             "description": "Application doesn't properly validate data crossing trust boundaries between components"},
            {"name": "Insufficient Workflow Validation", "category": "Insecure Design",
             "description": "Business logic flaws allow users to skip steps or manipulate multi-step processes"},
            {"name": "Missing Security Requirements", "category": "Insecure Design",
             "description": "Security controls not defined during design phase leading to fundamental architecture vulnerabilities"},
            # A05 — Security Misconfiguration
            {"name": "Default Credentials in Production", "category": "Security Misconfiguration",
             "description": "Default usernames and passwords not changed on production systems allowing easy unauthorized access"},
            {"name": "Unnecessary Features Enabled", "category": "Security Misconfiguration",
             "description": "Unused services, pages, accounts, or privileges enabled increasing attack surface"},
            {"name": "Directory Listing Enabled", "category": "Security Misconfiguration",
             "description": "Web server configured to show directory contents exposing sensitive files and application structure"},
            {"name": "Verbose Error Messages", "category": "Security Misconfiguration",
             "description": "Detailed error messages expose stack traces, database queries, or system information to attackers"},
            {"name": "Missing Security Headers", "category": "Security Misconfiguration",
             "description": "HTTP security headers (CSP, X-Frame-Options, HSTS) not configured leaving application vulnerable to attacks"},
            # A06 — Vulnerable and Outdated Components
            {"name": "Use of Components with Known Vulnerabilities", "category": "Vulnerable Components",
             "description": "Application uses outdated libraries, frameworks, or dependencies with publicly known security flaws"},
            {"name": "Lack of Dependency Scanning", "category": "Vulnerable Components",
             "description": "No automated scanning for vulnerable dependencies allowing outdated components to remain undetected"},
            {"name": "Unpatched Software", "category": "Vulnerable Components",
             "description": "Operating system, web server, or application server not regularly updated with security patches"},
            # A07 — Identification and Authentication Failures
            {"name": "Weak Password Policy", "category": "Authentication Failures",
             "description": "Application allows weak passwords without complexity requirements enabling brute force attacks"},
            {"name": "Missing Multi-Factor Authentication", "category": "Authentication Failures",
             "description": "Critical functions accessible with only password authentication making accounts vulnerable to credential theft"},
            {"name": "Session Fixation", "category": "Authentication Failures",
             "description": "Application doesn't regenerate session IDs after login allowing attackers to hijack authenticated sessions"},
            {"name": "Credential Stuffing Vulnerability", "category": "Authentication Failures",
             "description": "No protection against automated credential stuffing attacks using leaked password databases"},
            {"name": "Insecure Password Recovery", "category": "Authentication Failures",
             "description": "Password reset mechanism uses predictable tokens or security questions allowing account takeover"},
            # A08 — Software and Data Integrity Failures
            {"name": "Insecure Deserialization", "category": "Integrity Failures",
             "description": "Application deserializes untrusted data allowing remote code execution or privilege escalation"},
            {"name": "Missing Code Signing", "category": "Integrity Failures",
             "description": "Software updates not digitally signed allowing malicious code injection through compromised update mechanisms"},
            {"name": "CI/CD Pipeline Compromise", "category": "Integrity Failures",
             "description": "Insecure build pipeline allows attackers to inject malicious code during development or deployment"},
            {"name": "Lack of Integrity Verification", "category": "Integrity Failures",
             "description": "Application doesn't verify integrity of critical data or code allowing tampering to go undetected"},
            # A09 — Security Logging and Monitoring Failures
            {"name": "Insufficient Logging", "category": "Logging Failures",
             "description": "Security events (failed logins, access violations) not logged preventing detection of attacks"},
            {"name": "Log Injection", "category": "Logging Failures",
             "description": "User input logged without sanitization allowing attackers to forge log entries or inject malicious content"},
            {"name": "Missing Alerting for Critical Events", "category": "Logging Failures",
             "description": "No real-time alerts for suspicious activities delaying incident response"},
            {"name": "Logs Stored Insecurely", "category": "Logging Failures",
             "description": "Log files accessible to unauthorized users or stored without encryption exposing sensitive data"},
            # A10 — Server-Side Request Forgery
            {"name": "Server-Side Request Forgery", "category": "SSRF",
             "description": "Application fetches remote resources based on user input without validation, allowing access to internal systems"},
            {"name": "Internal Service Exposure via SSRF", "category": "SSRF",
             "description": "SSRF vulnerability allows scanning and accessing internal services not exposed to internet"},
            {"name": "Cloud Metadata Service Abuse", "category": "SSRF",
             "description": "SSRF used to access cloud metadata endpoints exposing credentials and configuration"},
        ],
        "mitigations": [
            {"name": "Implement Role-Based Access Control (RBAC)", "category": "Access Control",
             "description": "Define user roles and enforce permissions at every access point with deny-by-default principle"},
            {"name": "Use Indirect Object References", "category": "Access Control",
             "description": "Map direct object references to user-specific session data preventing unauthorized access"},
            {"name": "Enforce Access Control at API Layer", "category": "Access Control",
             "description": "Verify authorization for every API endpoint and resource access preventing privilege escalation"},
            {"name": "Use Strong Encryption Algorithms", "category": "Cryptography",
             "description": "Implement AES-256 for encryption and SHA-256 or better for hashing, avoid deprecated algorithms"},
            {"name": "Implement TLS 1.2+ with Strong Ciphers", "category": "Cryptography",
             "description": "Configure TLS 1.2 or 1.3 only with strong cipher suites, disable weak protocols"},
            {"name": "Use Key Management System (KMS)", "category": "Cryptography",
             "description": "Store encryption keys in dedicated KMS or hardware security modules, rotate regularly"},
            {"name": "Enforce HTTPS Everywhere", "category": "Cryptography",
             "description": "Redirect all HTTP traffic to HTTPS and implement HSTS header to prevent downgrade attacks"},
            {"name": "Use Parameterized Queries", "category": "Input Validation",
             "description": "Always use prepared statements with parameter binding for database queries preventing SQL injection"},
            {"name": "Input Validation and Sanitization", "category": "Input Validation",
             "description": "Validate all user input against whitelist patterns and sanitize before processing"},
            {"name": "Use ORM Frameworks Securely", "category": "Input Validation",
             "description": "Leverage ORM frameworks with parameterized queries, avoid raw SQL construction"},
            {"name": "Disable XML External Entity Processing", "category": "Input Validation",
             "description": "Configure XML parsers to disable external entity resolution preventing XXE attacks"},
            {"name": "Implement Rate Limiting", "category": "Secure Design",
             "description": "Apply throttling on authentication, API endpoints, and resource-intensive operations"},
            {"name": "Use Threat Modeling", "category": "Secure Design",
             "description": "Conduct threat modeling during design phase to identify and address security risks early"},
            {"name": "Implement Defense in Depth", "category": "Secure Design",
             "description": "Layer multiple security controls so failure of one doesn't compromise entire system"},
            {"name": "Harden Default Configurations", "category": "Configuration",
             "description": "Change all default credentials, disable unnecessary features, and follow security hardening guides"},
            {"name": "Implement Security Headers", "category": "Configuration",
             "description": "Configure CSP, X-Frame-Options, X-Content-Type-Options, HSTS, and other security headers"},
            {"name": "Disable Directory Listing", "category": "Configuration",
             "description": "Configure web server to prevent directory browsing and hide application structure"},
            {"name": "Use Custom Error Pages", "category": "Configuration",
             "description": "Display generic error messages to users while logging detailed errors securely"},
            {"name": "Implement Dependency Scanning", "category": "Supply Chain",
             "description": "Use automated tools (Snyk, Dependabot) to scan and alert on vulnerable dependencies"},
            {"name": "Establish Patch Management Process", "category": "Supply Chain",
             "description": "Regularly update all components and have process for emergency patching of critical vulnerabilities"},
            {"name": "Remove Unused Dependencies", "category": "Supply Chain",
             "description": "Regularly audit and remove unused libraries and components reducing attack surface"},
            {"name": "Implement Multi-Factor Authentication (MFA)", "category": "Authentication",
             "description": "Require MFA for all users, especially for administrative and sensitive operations"},
            {"name": "Enforce Strong Password Policy", "category": "Authentication",
             "description": "Require minimum 12 characters, complexity requirements, and check against breached password databases"},
            {"name": "Implement Account Lockout", "category": "Authentication",
             "description": "Lock accounts after failed login attempts with exponential backoff to prevent brute force"},
            {"name": "Regenerate Session IDs After Login", "category": "Authentication",
             "description": "Create new session ID upon authentication to prevent session fixation attacks"},
            {"name": "Implement Code Signing", "category": "Integrity",
             "description": "Digitally sign all software releases and verify signatures before deployment"},
            {"name": "Secure CI/CD Pipeline", "category": "Integrity",
             "description": "Harden build servers, require code review, and scan for vulnerabilities in pipeline"},
            {"name": "Avoid Unsafe Deserialization", "category": "Integrity",
             "description": "Use safe serialization formats (JSON) and validate deserialized data against schema"},
            {"name": "Implement Comprehensive Logging", "category": "Monitoring",
             "description": "Log all security events including authentication, authorization failures, and input validation errors"},
            {"name": "Centralize Log Management", "category": "Monitoring",
             "description": "Send logs to centralized SIEM system for correlation and long-term retention"},
            {"name": "Implement Real-Time Alerting", "category": "Monitoring",
             "description": "Configure alerts for suspicious patterns like multiple failed logins or privilege escalation attempts"},
            {"name": "Validate and Sanitize URLs", "category": "Input Validation",
             "description": "Whitelist allowed domains and protocols, validate URLs before making requests"},
            {"name": "Disable URL Redirects in Requests", "category": "Input Validation",
             "description": "Configure HTTP clients to not follow redirects automatically preventing SSRF bypass"},
            {"name": "Use Network Segmentation", "category": "Network Security",
             "description": "Isolate application servers from internal networks and restrict outbound connections"},
        ],
    },

    # ── LINDDUN ───────────────────────────────────────────────────────────────
    {
        "name": "LINDDUN",
        "description": (
            "LINDDUN Privacy Threat Modeling — Linkability, Identifiability, "
            "Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance"
        ),
        "threats": [
            # Linkability
            {"name": "User Activity Tracking Across Sessions", "category": "Linkability",
             "description": "Attacker correlates user activities across different sessions using persistent identifiers or browser fingerprinting"},
            {"name": "Cross-Site Tracking via Third-Party Cookies", "category": "Linkability",
             "description": "Third-party cookies and trackers link user behavior across multiple websites creating detailed profiles"},
            {"name": "Location Data Correlation", "category": "Linkability",
             "description": "GPS, IP address, or Wi-Fi data linked across time to track user movements and patterns"},
            {"name": "Device Fingerprinting", "category": "Linkability",
             "description": "Browser and device characteristics collected to create unique fingerprint enabling cross-session tracking"},
            # Identifiability
            {"name": "Username Enumeration", "category": "Identifiability",
             "description": "Application reveals whether usernames or email addresses exist through different error messages or timing attacks"},
            {"name": "PII Exposure in URLs", "category": "Identifiability",
             "description": "Personally identifiable information included in URLs visible in browser history, logs, and referrer headers"},
            {"name": "Metadata Exposure in Files", "category": "Identifiability",
             "description": "Uploaded files contain metadata (author, location, device info) revealing user identity"},
            {"name": "Re-identification via Data Aggregation", "category": "Identifiability",
             "description": "Combining supposedly anonymous data points allows identification of individuals"},
            # Non-repudiation
            {"name": "Insufficient Audit Logging", "category": "Non-repudiation",
             "description": "User actions not properly logged allowing users to deny performing sensitive operations"},
            {"name": "Missing Digital Signatures", "category": "Non-repudiation",
             "description": "Transactions lack cryptographic signatures allowing users to claim they didn't authorize actions"},
            {"name": "Shared Account Usage", "category": "Non-repudiation",
             "description": "Multiple users sharing single account preventing attribution of specific actions to individuals"},
            # Detectability
            {"name": "Social Media Presence Linkage", "category": "Detectability",
             "description": "User profiles linkable to social media accounts revealing additional personal information"},
            {"name": "Public Data Aggregation", "category": "Detectability",
             "description": "Publicly accessible user data aggregated to build comprehensive profiles without consent"},
            {"name": "Pattern Analysis Revealing Behavior", "category": "Detectability",
             "description": "Analysis of usage patterns reveals sensitive information about user behavior and preferences"},
            # Disclosure of Information
            {"name": "Insufficient Data Anonymization", "category": "Disclosure",
             "description": "Personal data not properly anonymized before sharing with third parties or for analytics"},
            {"name": "Excessive Data Collection", "category": "Disclosure",
             "description": "Application collects more personal data than necessary for stated purposes"},
            {"name": "Insecure Data Sharing with Third Parties", "category": "Disclosure",
             "description": "Personal data shared with partners or vendors without proper security controls or user consent"},
            {"name": "Data Breach via Database Exposure", "category": "Disclosure",
             "description": "Personal data exposed through database vulnerabilities or misconfigurations"},
            {"name": "Sensitive Data in Client-Side Code", "category": "Disclosure",
             "description": "Personal or sensitive information embedded in JavaScript or HTML accessible to anyone"},
            # Unawareness
            {"name": "Unclear Privacy Policy", "category": "Unawareness",
             "description": "Privacy policy written in complex legal language preventing users from understanding data practices"},
            {"name": "Hidden Data Collection", "category": "Unawareness",
             "description": "Application collects data without informing users or obtaining consent"},
            {"name": "Lack of Data Access Controls", "category": "Unawareness",
             "description": "Users cannot view, export, or delete their personal data as required by privacy regulations"},
            {"name": "Missing Privacy-Enhancing Features", "category": "Unawareness",
             "description": "No options for users to limit data collection or control privacy settings"},
            # Non-compliance
            {"name": "GDPR Violation - Missing Legal Basis", "category": "Non-compliance",
             "description": "Personal data processed without valid legal basis (consent, contract, legitimate interest)"},
            {"name": "GDPR Violation - Data Retention", "category": "Non-compliance",
             "description": "Personal data retained longer than necessary violating data minimization principle"},
            {"name": "CCPA Violation - Consumer Rights", "category": "Non-compliance",
             "description": "Application doesn't provide required mechanisms for users to exercise CCPA rights"},
            {"name": "Missing Data Protection Impact Assessment", "category": "Non-compliance",
             "description": "High-risk processing activities conducted without required DPIA under GDPR"},
            {"name": "International Data Transfer Violation", "category": "Non-compliance",
             "description": "Personal data transferred internationally without adequate safeguards (SCCs, BCRs)"},
        ],
        "mitigations": [
            {"name": "Implement Cookie Consent Management", "category": "Privacy Controls",
             "description": "Use consent management platform to control tracking cookies and respect user privacy choices"},
            {"name": "Rotate Session Identifiers", "category": "Privacy Controls",
             "description": "Regularly rotate session IDs and use short-lived tokens to prevent long-term tracking"},
            {"name": "Block Third-Party Trackers", "category": "Privacy Controls",
             "description": "Implement Content Security Policy to block third-party tracking scripts and analytics"},
            {"name": "Minimize Browser Fingerprinting", "category": "Privacy Controls",
             "description": "Reduce uniqueness of browser characteristics and randomize canvas fingerprints"},
            {"name": "Use Generic Error Messages", "category": "Data Protection",
             "description": "Return same error message for all authentication failures preventing username enumeration"},
            {"name": "Strip Metadata from Files", "category": "Data Protection",
             "description": "Remove EXIF and metadata from user-uploaded files before storage or display"},
            {"name": "Implement k-Anonymity", "category": "Data Protection",
             "description": "Ensure data releases maintain k-anonymity preventing re-identification of individuals"},
            {"name": "Use Pseudonymization", "category": "Data Protection",
             "description": "Replace direct identifiers with pseudonyms making data attribution impossible without additional information"},
            {"name": "Implement Comprehensive Audit Trails", "category": "Accountability",
             "description": "Log all user actions with timestamps and digital signatures for accountability"},
            {"name": "Use Digital Signatures for Transactions", "category": "Accountability",
             "description": "Require cryptographic signatures for sensitive operations providing proof of authorization"},
            {"name": "Enforce Individual User Accounts", "category": "Accountability",
             "description": "Prohibit account sharing and require unique credentials for each user"},
            {"name": "Implement Access Controls on Profiles", "category": "Privacy Controls",
             "description": "Allow users to control visibility of profile information and limit public data exposure"},
            {"name": "Provide Privacy Settings Dashboard", "category": "Privacy Controls",
             "description": "Give users granular control over what data is public, shared, or private"},
            {"name": "Use Differential Privacy", "category": "Data Protection",
             "description": "Add statistical noise to aggregated data preventing individual pattern detection"},
            {"name": "Implement Data Minimization", "category": "Data Protection",
             "description": "Collect only data essential for stated purposes and delete when no longer needed"},
            {"name": "Encrypt Personal Data at Rest", "category": "Data Protection",
             "description": "Use AES-256 encryption for all stored personal data with proper key management"},
            {"name": "Use Data Processing Agreements", "category": "Compliance",
             "description": "Establish formal DPAs with all data processors ensuring GDPR compliance"},
            {"name": "Implement Purpose Limitation", "category": "Compliance",
             "description": "Use data only for explicitly stated purposes and obtain new consent for new uses"},
            {"name": "Provide Clear Privacy Notices", "category": "Transparency",
             "description": "Write privacy policy in plain language explaining data collection, use, and rights"},
            {"name": "Implement Just-in-Time Notices", "category": "Transparency",
             "description": "Show privacy notices at point of data collection explaining why data is needed"},
            {"name": "Build User Data Dashboard", "category": "Transparency",
             "description": "Allow users to view all collected data, download it, and request deletion"},
            {"name": "Provide Privacy-Enhancing Settings", "category": "Privacy Controls",
             "description": "Offer privacy modes, anonymous browsing, and data collection opt-outs"},
            {"name": "Conduct Data Protection Impact Assessment", "category": "Compliance",
             "description": "Perform DPIA for high-risk processing activities as required by GDPR Article 35"},
            {"name": "Implement Standard Contractual Clauses", "category": "Compliance",
             "description": "Use SCCs for international data transfers ensuring adequate data protection"},
            {"name": "Establish Data Retention Policies", "category": "Compliance",
             "description": "Define and enforce retention periods for different data types with automated deletion"},
            {"name": "Appoint Data Protection Officer", "category": "Compliance",
             "description": "Designate DPO responsible for GDPR compliance and data protection strategy"},
            {"name": "Implement Consent Management", "category": "Compliance",
             "description": "Build system to obtain, record, and respect user consent for data processing"},
        ],
    },
]


# ── Seeder ────────────────────────────────────────────────────────────────────

def _seed_framework(db: Session, fw: dict) -> None:
    """Seed one framework — creates it if missing, then upserts threats and mitigations by name."""
    # Get or create framework
    framework = db.query(Framework).filter(Framework.name == fw["name"]).first()
    if not framework:
        framework = Framework(name=fw["name"], description=fw.get("description", ""))
        db.add(framework)
        db.commit()
        db.refresh(framework)
        logger.info("  Created framework: %s", fw["name"])
    else:
        logger.debug("  Framework already exists: %s", fw["name"])

    # Seed threats (skip entries that already exist by name)
    existing_threat_names = {
        row[0]
        for row in db.query(Threat.name).filter(Threat.framework_id == framework.id).all()
    }
    new_threats = [
        Threat(framework_id=framework.id, is_custom=False, **t)
        for t in fw["threats"]
        if t["name"] not in existing_threat_names
    ]
    if new_threats:
        db.bulk_save_objects(new_threats)
        logger.info("  Added %d threats to '%s'", len(new_threats), fw["name"])

    # Seed mitigations (skip entries that already exist by name)
    existing_mitigation_names = {
        row[0]
        for row in db.query(Mitigation.name).filter(Mitigation.framework_id == framework.id).all()
    }
    new_mitigations = [
        Mitigation(framework_id=framework.id, is_custom=False, **m)
        for m in fw["mitigations"]
        if m["name"] not in existing_mitigation_names
    ]
    if new_mitigations:
        db.bulk_save_objects(new_mitigations)
        logger.info("  Added %d mitigations to '%s'", len(new_mitigations), fw["name"])

    db.commit()


def seed_knowledge_base() -> None:
    """
    Seed all registered frameworks, threats, and mitigations.

    Safe to call on every startup — existing entries are never duplicated or
    overwritten.  New entries in FRAMEWORKS_REGISTRY are inserted automatically.
    """
    db = SessionLocal()
    try:
        logger.info("Seeding knowledge base (%d frameworks)…", len(FRAMEWORKS_REGISTRY))
        for fw in FRAMEWORKS_REGISTRY:
            _seed_framework(db, fw)
        logger.info("Knowledge base seeding complete.")
    except Exception:
        db.rollback()
        logger.exception("Knowledge base seeding failed — rolled back.")
        raise
    finally:
        db.close()
