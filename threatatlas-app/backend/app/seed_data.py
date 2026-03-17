"""Seed data for knowledge base - STRIDE and PASTA frameworks with threats and mitigations."""

FRAMEWORKS = [
    {
        "name": "STRIDE",
        "description": "STRIDE is a threat modeling methodology developed by Microsoft. It stands for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege."
    },
    {
        "name": "PASTA",
        "description": "Process for Attack Simulation and Threat Analysis (PASTA) is a risk-centric threat modeling methodology that provides a seven-stage process for aligning business objectives and technical requirements."
    }
]

STRIDE_THREATS = [
    {
        "name": "Spoofing Identity",
        "description": "Pretending to be someone or something else",
        "category": "Spoofing"
    },
    {
        "name": "User Impersonation",
        "description": "Attacker impersonates a legitimate user to gain unauthorized access",
        "category": "Spoofing"
    },
    {
        "name": "Data Tampering",
        "description": "Malicious modification of data",
        "category": "Tampering"
    },
    {
        "name": "Code Injection",
        "description": "Injecting malicious code into application (SQL injection, XSS, etc.)",
        "category": "Tampering"
    },
    {
        "name": "Man-in-the-Middle Attack",
        "description": "Intercepting and potentially altering communication between two parties",
        "category": "Tampering"
    },
    {
        "name": "Repudiation of Actions",
        "description": "User denies performing an action without ability to prove otherwise",
        "category": "Repudiation"
    },
    {
        "name": "Information Disclosure",
        "description": "Exposure of information to unauthorized individuals",
        "category": "Information Disclosure"
    },
    {
        "name": "Data Breach",
        "description": "Unauthorized access to sensitive or confidential data",
        "category": "Information Disclosure"
    },
    {
        "name": "Denial of Service (DoS)",
        "description": "Denying service to valid users",
        "category": "Denial of Service"
    },
    {
        "name": "Resource Exhaustion",
        "description": "Consuming all available resources to prevent legitimate use",
        "category": "Denial of Service"
    },
    {
        "name": "Elevation of Privilege",
        "description": "Gaining capabilities without proper authorization",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Privilege Escalation",
        "description": "Exploiting a vulnerability to gain elevated access to resources",
        "category": "Elevation of Privilege"
    }
]

STRIDE_MITIGATIONS = [
    {
        "name": "Multi-Factor Authentication",
        "description": "Implement MFA to verify user identity",
        "category": "Spoofing"
    },
    {
        "name": "Digital Signatures",
        "description": "Use digital signatures to verify authenticity",
        "category": "Spoofing"
    },
    {
        "name": "Input Validation",
        "description": "Validate and sanitize all user inputs",
        "category": "Tampering"
    },
    {
        "name": "Data Integrity Checks",
        "description": "Implement checksums and hash functions to detect tampering",
        "category": "Tampering"
    },
    {
        "name": "Encryption in Transit",
        "description": "Use TLS/SSL to encrypt data during transmission",
        "category": "Tampering"
    },
    {
        "name": "Audit Logging",
        "description": "Maintain comprehensive logs of all actions",
        "category": "Repudiation"
    },
    {
        "name": "Secure Timestamps",
        "description": "Use trusted time sources for all transactions",
        "category": "Repudiation"
    },
    {
        "name": "Data Encryption at Rest",
        "description": "Encrypt sensitive data when stored",
        "category": "Information Disclosure"
    },
    {
        "name": "Access Control Lists (ACLs)",
        "description": "Implement proper access controls to limit data exposure",
        "category": "Information Disclosure"
    },
    {
        "name": "Rate Limiting",
        "description": "Limit the rate of requests to prevent resource exhaustion",
        "category": "Denial of Service"
    },
    {
        "name": "Resource Quotas",
        "description": "Implement quotas to prevent single users from consuming all resources",
        "category": "Denial of Service"
    },
    {
        "name": "Principle of Least Privilege",
        "description": "Grant users only the minimum necessary permissions",
        "category": "Elevation of Privilege"
    },
    {
        "name": "Role-Based Access Control (RBAC)",
        "description": "Implement RBAC to manage user permissions systematically",
        "category": "Elevation of Privilege"
    }
]

PASTA_THREATS = [
    {
        "name": "Business Logic Bypass",
        "description": "Circumventing intended business logic flows",
        "category": "Attack Simulation"
    },
    {
        "name": "API Abuse",
        "description": "Misuse of API endpoints for malicious purposes",
        "category": "Attack Simulation"
    },
    {
        "name": "Session Hijacking",
        "description": "Stealing or predicting session tokens",
        "category": "Attack Simulation"
    },
    {
        "name": "Credential Stuffing",
        "description": "Using stolen credentials from one service on another",
        "category": "Attack Simulation"
    },
    {
        "name": "Cross-Site Scripting (XSS)",
        "description": "Injecting malicious scripts into web pages",
        "category": "Attack Simulation"
    },
    {
        "name": "Cross-Site Request Forgery (CSRF)",
        "description": "Forcing users to execute unwanted actions",
        "category": "Attack Simulation"
    }
]

PASTA_MITIGATIONS = [
    {
        "name": "Business Logic Validation",
        "description": "Implement server-side validation of business rules",
        "category": "Attack Simulation"
    },
    {
        "name": "API Gateway",
        "description": "Use an API gateway to control and monitor API access",
        "category": "Attack Simulation"
    },
    {
        "name": "Secure Session Management",
        "description": "Use secure, random session tokens with proper timeout",
        "category": "Attack Simulation"
    },
    {
        "name": "Password Policy Enforcement",
        "description": "Enforce strong password requirements and detection of compromised passwords",
        "category": "Attack Simulation"
    },
    {
        "name": "Content Security Policy (CSP)",
        "description": "Implement CSP headers to prevent XSS attacks",
        "category": "Attack Simulation"
    },
    {
        "name": "Anti-CSRF Tokens",
        "description": "Use CSRF tokens to validate legitimate requests",
        "category": "Attack Simulation"
    }
]
