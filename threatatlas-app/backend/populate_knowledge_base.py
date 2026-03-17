"""
Populate the knowledge base with comprehensive threat modeling data.
Run this script to add realistic threats and mitigations.
"""
from app.database import SessionLocal
from app.models import Framework, Threat, Mitigation

# STRIDE Framework Threats
STRIDE_THREATS = [
    # Spoofing
    {
        "name": "Credential Theft via Phishing",
        "description": "Attacker sends phishing emails to steal user credentials by impersonating legitimate services",
        "category": "Spoofing"
    },
    {
        "name": "Session Hijacking",
        "description": "Attacker steals or predicts session tokens to impersonate authenticated users",
        "category": "Spoofing"
    },
    {
        "name": "Man-in-the-Middle Attack",
        "description": "Attacker intercepts communication between client and server to steal credentials or session data",
        "category": "Spoofing"
    },
    {
        "name": "IP Spoofing",
        "description": "Attacker forges source IP address to bypass IP-based authentication or hide identity",
        "category": "Spoofing"
    },
    {
        "name": "DNS Spoofing",
        "description": "Attacker corrupts DNS cache to redirect users to malicious websites",
        "category": "Spoofing"
    },

    # Tampering
    {
        "name": "SQL Injection",
        "description": "Attacker injects malicious SQL code through user inputs to manipulate database queries",
        "category": "Tampering"
    },
    {
        "name": "Cross-Site Scripting (XSS)",
        "description": "Attacker injects malicious scripts into web pages viewed by other users",
        "category": "Tampering"
    },
    {
        "name": "Parameter Tampering",
        "description": "Attacker modifies URL parameters, form fields, or cookies to manipulate application behavior",
        "category": "Tampering"
    },
    {
        "name": "Code Injection",
        "description": "Attacker injects malicious code into application to execute arbitrary commands",
        "category": "Tampering"
    },
    {
        "name": "File Upload Exploitation",
        "description": "Attacker uploads malicious files to compromise server or execute code",
        "category": "Tampering"
    },
    {
        "name": "Configuration File Manipulation",
        "description": "Attacker modifies configuration files to alter application behavior or gain elevated privileges",
        "category": "Tampering"
    },

    # Repudiation
    {
        "name": "Insufficient Audit Logging",
        "description": "Critical actions are not logged, allowing attackers to perform malicious activities without detection",
        "category": "Repudiation"
    },
    {
        "name": "Log Tampering",
        "description": "Attacker modifies or deletes audit logs to hide malicious activities",
        "category": "Repudiation"
    },
    {
        "name": "Transaction Denial",
        "description": "User denies performing a transaction due to lack of non-repudiation controls",
        "category": "Repudiation"
    },
    {
        "name": "Clock Manipulation",
        "description": "Attacker manipulates system time to falsify timestamps in logs and transactions",
        "category": "Repudiation"
    },

    # Information Disclosure
    {
        "name": "Sensitive Data Exposure in Logs",
        "description": "Application logs contain sensitive information like passwords, tokens, or PII",
        "category": "Information Disclosure"
    },
    {
        "name": "Directory Traversal",
        "description": "Attacker accesses files outside intended directory by manipulating file paths",
        "category": "Information Disclosure"
    },
    {
        "name": "Insecure Direct Object References",
        "description": "Application exposes internal object references allowing unauthorized access to data",
        "category": "Information Disclosure"
    },
    {
        "name": "Information Leakage via Error Messages",
        "description": "Detailed error messages reveal sensitive system information to attackers",
        "category": "Information Disclosure"
    },
    {
        "name": "Unencrypted Data Transmission",
        "description": "Sensitive data transmitted over network without encryption can be intercepted",
        "category": "Information Disclosure"
    },
    {
        "name": "Metadata Exposure",
        "description": "Application exposes sensitive metadata in HTTP headers, comments, or API responses",
        "category": "Information Disclosure"
    },
    {
        "name": "Memory Dump Exposure",
        "description": "Sensitive data in memory dumps can be accessed by unauthorized users",
        "category": "Information Disclosure"
    },

    # Denial of Service
    {
        "name": "Resource Exhaustion Attack",
        "description": "Attacker consumes system resources (CPU, memory, disk) to make service unavailable",
        "category": "Denial of Service"
    },
    {
        "name": "Application-Layer DDoS",
        "description": "Attacker floods application with legitimate-looking requests to overwhelm servers",
        "category": "Denial of Service"
    },
    {
        "name": "Regex Denial of Service (ReDoS)",
        "description": "Attacker exploits inefficient regular expressions to cause catastrophic backtracking",
        "category": "Denial of Service"
    },
    {
        "name": "Database Connection Pool Exhaustion",
        "description": "Attacker opens many database connections until pool is exhausted",
        "category": "Denial of Service"
    },
    {
        "name": "XML Bomb (Billion Laughs)",
        "description": "Attacker sends malicious XML with recursive entity expansion to exhaust memory",
        "category": "Denial of Service"
    },
    {
        "name": "Slowloris Attack",
        "description": "Attacker sends partial HTTP requests slowly to keep connections open and exhaust server",
        "category": "Denial of Service"
    },

    # Elevation of Privilege
    {
        "name": "Privilege Escalation via IDOR",
        "description": "Attacker manipulates object references to access resources belonging to higher-privileged users",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Authentication Bypass",
        "description": "Attacker circumvents authentication mechanisms to gain unauthorized access",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Authorization Bypass",
        "description": "Attacker bypasses authorization checks to access restricted functionality",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Cross-Site Request Forgery (CSRF)",
        "description": "Attacker tricks authenticated user into performing unwanted actions",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Insecure Deserialization",
        "description": "Attacker exploits deserialization to execute arbitrary code or escalate privileges",
        "category": "Elevation of Privilege"
    },
    {
        "name": "JWT Token Manipulation",
        "description": "Attacker modifies JWT claims to escalate privileges or impersonate users",
        "category": "Elevation of Privilege"
    },
]

# STRIDE Framework Mitigations
STRIDE_MITIGATIONS = [
    # Spoofing Mitigations
    {
        "name": "Multi-Factor Authentication (MFA)",
        "description": "Implement MFA requiring multiple verification factors (password, OTP, biometrics) to prevent credential theft",
        "category": "Spoofing"
    },
    {
        "name": "Certificate-Based Authentication",
        "description": "Use digital certificates for mutual TLS authentication to verify identity of both parties",
        "category": "Spoofing"
    },
    {
        "name": "Secure Session Management",
        "description": "Implement secure session tokens with proper expiration, rotation, and HTTPOnly/Secure flags",
        "category": "Spoofing"
    },
    {
        "name": "TLS/SSL Encryption",
        "description": "Enforce HTTPS with TLS 1.2+ to protect against man-in-the-middle attacks",
        "category": "Spoofing"
    },
    {
        "name": "DNSSEC Implementation",
        "description": "Use DNSSEC to authenticate DNS responses and prevent DNS spoofing",
        "category": "Spoofing"
    },

    # Tampering Mitigations
    {
        "name": "Input Validation and Sanitization",
        "description": "Validate and sanitize all user inputs using allowlists and proper encoding",
        "category": "Tampering"
    },
    {
        "name": "Parameterized Queries",
        "description": "Use prepared statements with parameterized queries to prevent SQL injection",
        "category": "Tampering"
    },
    {
        "name": "Content Security Policy (CSP)",
        "description": "Implement CSP headers to prevent XSS attacks by controlling resource loading",
        "category": "Tampering"
    },
    {
        "name": "Digital Signatures",
        "description": "Use cryptographic signatures to verify data integrity and detect tampering",
        "category": "Tampering"
    },
    {
        "name": "File Upload Restrictions",
        "description": "Implement file type validation, size limits, and virus scanning for uploads",
        "category": "Tampering"
    },
    {
        "name": "Code Signing",
        "description": "Sign application code and verify signatures to prevent code injection",
        "category": "Tampering"
    },

    # Repudiation Mitigations
    {
        "name": "Comprehensive Audit Logging",
        "description": "Log all critical operations with timestamps, user identity, and action details",
        "category": "Repudiation"
    },
    {
        "name": "Tamper-Proof Log Storage",
        "description": "Store logs in append-only systems or use blockchain for immutable audit trails",
        "category": "Repudiation"
    },
    {
        "name": "Digital Transaction Signatures",
        "description": "Require cryptographic signatures for critical transactions to ensure non-repudiation",
        "category": "Repudiation"
    },
    {
        "name": "Secure Time Synchronization",
        "description": "Use NTP with authentication to maintain accurate timestamps across systems",
        "category": "Repudiation"
    },
    {
        "name": "Log Integrity Monitoring",
        "description": "Implement SIEM solutions to detect log tampering and unauthorized modifications",
        "category": "Repudiation"
    },

    # Information Disclosure Mitigations
    {
        "name": "Data Encryption at Rest",
        "description": "Encrypt sensitive data stored in databases and file systems using AES-256",
        "category": "Information Disclosure"
    },
    {
        "name": "Data Encryption in Transit",
        "description": "Use TLS/SSL for all data transmission to prevent interception",
        "category": "Information Disclosure"
    },
    {
        "name": "Access Control Lists (ACLs)",
        "description": "Implement fine-grained access controls to restrict data access based on user roles",
        "category": "Information Disclosure"
    },
    {
        "name": "Secure Error Handling",
        "description": "Implement generic error messages for users while logging detailed errors securely",
        "category": "Information Disclosure"
    },
    {
        "name": "Data Masking and Redaction",
        "description": "Mask sensitive data in logs, UI, and API responses to prevent exposure",
        "category": "Information Disclosure"
    },
    {
        "name": "Security Headers",
        "description": "Implement security headers (X-Content-Type-Options, X-Frame-Options, etc.) to prevent information leakage",
        "category": "Information Disclosure"
    },

    # Denial of Service Mitigations
    {
        "name": "Rate Limiting",
        "description": "Implement rate limiting per user/IP to prevent resource exhaustion attacks",
        "category": "Denial of Service"
    },
    {
        "name": "Web Application Firewall (WAF)",
        "description": "Deploy WAF to filter malicious traffic and protect against application-layer attacks",
        "category": "Denial of Service"
    },
    {
        "name": "Connection Pooling",
        "description": "Implement connection pools with proper limits and timeouts to prevent exhaustion",
        "category": "Denial of Service"
    },
    {
        "name": "Input Size Limits",
        "description": "Enforce maximum size limits on requests, uploads, and XML/JSON payloads",
        "category": "Denial of Service"
    },
    {
        "name": "Auto-Scaling",
        "description": "Implement auto-scaling to handle traffic spikes and distribute load",
        "category": "Denial of Service"
    },
    {
        "name": "Request Timeout Configuration",
        "description": "Set appropriate timeouts for connections and requests to prevent slowloris attacks",
        "category": "Denial of Service"
    },

    # Elevation of Privilege Mitigations
    {
        "name": "Role-Based Access Control (RBAC)",
        "description": "Implement RBAC to ensure users only access resources appropriate for their role",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Principle of Least Privilege",
        "description": "Grant minimum necessary permissions to users and services",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Authorization Checks",
        "description": "Verify user permissions for every protected resource and action",
        "category": "Elevation of Privilege"
    },
    {
        "name": "CSRF Tokens",
        "description": "Implement anti-CSRF tokens for all state-changing operations",
        "category": "Elevation of Privilege"
    },
    {
        "name": "JWT Signature Verification",
        "description": "Verify JWT signatures and validate claims before trusting token data",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Secure Deserialization",
        "description": "Avoid deserializing untrusted data or use safe serialization formats like JSON",
        "category": "Elevation of Privilege"
    },
]

# PASTA Framework Threats
PASTA_THREATS = [
    {
        "name": "API Key Exposure in Client-Side Code",
        "description": "API keys or secrets hardcoded in frontend code can be extracted by attackers",
        "category": "Asset Analysis"
    },
    {
        "name": "Insufficient API Authentication",
        "description": "API endpoints lack proper authentication allowing unauthorized access",
        "category": "Attack Surface Analysis"
    },
    {
        "name": "Mass Assignment Vulnerability",
        "description": "API allows modification of object properties that should be restricted",
        "category": "Attack Modeling"
    },
    {
        "name": "Broken Object Level Authorization",
        "description": "API fails to validate user ownership of resources before allowing access",
        "category": "Threat Analysis"
    },
    {
        "name": "Excessive Data Exposure",
        "description": "API returns more data than necessary, exposing sensitive information",
        "category": "Vulnerability Analysis"
    },
    {
        "name": "Lack of Rate Limiting on Sensitive Operations",
        "description": "No rate limiting on password reset, account creation, or financial transactions",
        "category": "Attack Modeling"
    },
    {
        "name": "Insecure Direct Object References in APIs",
        "description": "Predictable resource IDs allow enumeration and unauthorized access",
        "category": "Threat Analysis"
    },
    {
        "name": "GraphQL Query Depth Attack",
        "description": "Deeply nested GraphQL queries exhaust server resources",
        "category": "Attack Surface Analysis"
    },
    {
        "name": "WebSocket Connection Hijacking",
        "description": "Unprotected WebSocket connections allow message interception or injection",
        "category": "Attack Modeling"
    },
    {
        "name": "Server-Side Request Forgery (SSRF)",
        "description": "Attacker tricks server into making requests to internal systems",
        "category": "Threat Analysis"
    },
]

# PASTA Framework Mitigations
PASTA_MITIGATIONS = [
    {
        "name": "Environment Variable Management",
        "description": "Store secrets in environment variables or secret management systems, never in code",
        "category": "Asset Analysis"
    },
    {
        "name": "API Gateway with Authentication",
        "description": "Implement API gateway with OAuth2/JWT authentication for all endpoints",
        "category": "Attack Surface Analysis"
    },
    {
        "name": "DTO Validation and Whitelisting",
        "description": "Use Data Transfer Objects with explicit property whitelisting to prevent mass assignment",
        "category": "Attack Modeling"
    },
    {
        "name": "Object-Level Authorization Checks",
        "description": "Verify user ownership before allowing access to any resource",
        "category": "Threat Analysis"
    },
    {
        "name": "Response Filtering",
        "description": "Filter API responses to return only necessary fields using DTOs or GraphQL field selection",
        "category": "Vulnerability Analysis"
    },
    {
        "name": "Distributed Rate Limiting",
        "description": "Implement Redis-based distributed rate limiting across all API instances",
        "category": "Attack Modeling"
    },
    {
        "name": "UUID-Based Resource Identifiers",
        "description": "Use UUIDs instead of sequential IDs to prevent enumeration attacks",
        "category": "Threat Analysis"
    },
    {
        "name": "GraphQL Query Complexity Analysis",
        "description": "Implement query depth and complexity limits for GraphQL endpoints",
        "category": "Attack Surface Analysis"
    },
    {
        "name": "WebSocket Authentication and Validation",
        "description": "Authenticate WebSocket connections and validate all messages",
        "category": "Attack Modeling"
    },
    {
        "name": "SSRF Protection with URL Validation",
        "description": "Validate and whitelist allowed URLs, disable URL redirects, and use internal DNS filtering",
        "category": "Threat Analysis"
    },
]


def populate_knowledge_base():
    """Populate the database with comprehensive threat modeling data."""
    db = SessionLocal()

    try:
        # Get frameworks
        stride = db.query(Framework).filter(Framework.name == "STRIDE").first()
        pasta = db.query(Framework).filter(Framework.name == "PASTA").first()

        if not stride or not pasta:
            print("Error: STRIDE or PASTA framework not found in database")
            return

        print(f"📚 Populating knowledge base...")
        print(f"STRIDE Framework ID: {stride.id}")
        print(f"PASTA Framework ID: {pasta.id}")

        # Add STRIDE threats
        print(f"\n🔴 Adding {len(STRIDE_THREATS)} STRIDE threats...")
        for threat_data in STRIDE_THREATS:
            existing = db.query(Threat).filter(
                Threat.framework_id == stride.id,
                Threat.name == threat_data["name"]
            ).first()

            if not existing:
                threat = Threat(
                    framework_id=stride.id,
                    name=threat_data["name"],
                    description=threat_data["description"],
                    category=threat_data["category"],
                    is_custom=False
                )
                db.add(threat)
                print(f"  ✓ Added: {threat_data['name']}")
            else:
                print(f"  ⊘ Skipped (exists): {threat_data['name']}")

        # Add STRIDE mitigations
        print(f"\n🟢 Adding {len(STRIDE_MITIGATIONS)} STRIDE mitigations...")
        for mitigation_data in STRIDE_MITIGATIONS:
            existing = db.query(Mitigation).filter(
                Mitigation.framework_id == stride.id,
                Mitigation.name == mitigation_data["name"]
            ).first()

            if not existing:
                mitigation = Mitigation(
                    framework_id=stride.id,
                    name=mitigation_data["name"],
                    description=mitigation_data["description"],
                    category=mitigation_data["category"],
                    is_custom=False
                )
                db.add(mitigation)
                print(f"  ✓ Added: {mitigation_data['name']}")
            else:
                print(f"  ⊘ Skipped (exists): {mitigation_data['name']}")

        # Add PASTA threats
        print(f"\n🔴 Adding {len(PASTA_THREATS)} PASTA threats...")
        for threat_data in PASTA_THREATS:
            existing = db.query(Threat).filter(
                Threat.framework_id == pasta.id,
                Threat.name == threat_data["name"]
            ).first()

            if not existing:
                threat = Threat(
                    framework_id=pasta.id,
                    name=threat_data["name"],
                    description=threat_data["description"],
                    category=threat_data["category"],
                    is_custom=False
                )
                db.add(threat)
                print(f"  ✓ Added: {threat_data['name']}")
            else:
                print(f"  ⊘ Skipped (exists): {threat_data['name']}")

        # Add PASTA mitigations
        print(f"\n🟢 Adding {len(PASTA_MITIGATIONS)} PASTA mitigations...")
        for mitigation_data in PASTA_MITIGATIONS:
            existing = db.query(Mitigation).filter(
                Mitigation.framework_id == pasta.id,
                Mitigation.name == mitigation_data["name"]
            ).first()

            if not existing:
                mitigation = Mitigation(
                    framework_id=pasta.id,
                    name=mitigation_data["name"],
                    description=mitigation_data["description"],
                    category=mitigation_data["category"],
                    is_custom=False
                )
                db.add(mitigation)
                print(f"  ✓ Added: {mitigation_data['name']}")
            else:
                print(f"  ⊘ Skipped (exists): {mitigation_data['name']}")

        # Commit all changes
        db.commit()

        # Print summary
        total_stride_threats = db.query(Threat).filter(Threat.framework_id == stride.id).count()
        total_stride_mitigations = db.query(Mitigation).filter(Mitigation.framework_id == stride.id).count()
        total_pasta_threats = db.query(Threat).filter(Threat.framework_id == pasta.id).count()
        total_pasta_mitigations = db.query(Mitigation).filter(Mitigation.framework_id == pasta.id).count()

        print("\n" + "="*60)
        print("✅ Knowledge Base Population Complete!")
        print("="*60)
        print(f"\nSTRIDE Framework:")
        print(f"  • Threats: {total_stride_threats}")
        print(f"  • Mitigations: {total_stride_mitigations}")
        print(f"\nPASTA Framework:")
        print(f"  • Threats: {total_pasta_threats}")
        print(f"  • Mitigations: {total_pasta_mitigations}")
        print(f"\nTotal Items: {total_stride_threats + total_stride_mitigations + total_pasta_threats + total_pasta_mitigations}")
        print("="*60)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_knowledge_base()
