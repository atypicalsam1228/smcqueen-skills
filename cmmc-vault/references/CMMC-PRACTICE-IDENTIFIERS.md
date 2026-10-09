# CMMC Practice Identifiers Reference

Use this file to match content to the correct CMMC practice domain, practice ID, and corresponding NIST SP 800-171 control.

## CMMC v2.0 Practice Domains

| Abbreviation | Domain Name | Wiki Domain Tag |
|---|---|---|
| AC | Access Control | access-control |
| AM | Asset Management | asset-management |
| AU | Audit and Accountability | audit-accountability |
| CM | Configuration Management | configuration-management |
| IA | Identification and Authentication | identification-auth |
| IR | Incident Response | incident-response |
| MA | Maintenance | maintenance |
| MP | Media Protection | media-protection |
| PS | Personnel Security | personnel-security |
| PE | Physical Protection | physical-protection |
| RE | Recovery | recovery |
| RM | Risk Management | risk-management |
| CA | Security Assessment | security-assessment |
| SA | Situational Awareness | situational-awareness |
| SC | System and Communications Protection | system-comms-protection |
| SI | System and Information Integrity | system-info-integrity |

## CMMC Level Coverage

- **Level 1** (17 practices): Foundational — FAR 52.204-21 requirements
- **Level 2** (110 practices): Advanced — NIST SP 800-171 Rev 2 requirements
- **Level 3** (134 practices): Expert — NIST SP 800-172 delta requirements

## Practice ID Format

```
<DOMAIN>.<LEVEL>.<SEQUENCE>

Examples:
  AC.1.001   — Access Control, Level 1, Practice 001
  CM.2.061   — Configuration Management, Level 2, Practice 061
  IA.3.083   — Identification & Authentication, Level 3, Practice 083
```

## NIST SP 800-171 Rev 2 Control Mapping

| Practice ID | NIST 800-171 Control | Description |
|---|---|---|
| AC.1.001 | 3.1.1 | Limit system access to authorized users |
| AC.1.002 | 3.1.2 | Limit system access to authorized transactions and functions |
| AC.2.005 | 3.1.3 | Control the flow of CUI in accordance with approved authorizations |
| AC.2.006 | 3.1.4 | Separate duties of individuals to reduce risk of malevolent activity |
| AC.2.007 | 3.1.5 | Employ the principle of least privilege |
| AC.2.008 | 3.1.6 | Use non-privileged accounts when accessing non-security functions |
| AC.2.009 | 3.1.7 | Prevent non-privileged users from executing privileged functions |
| AC.2.010 | 3.1.8 | Limit unsuccessful logon attempts |
| AC.2.011 | 3.1.9 | Provide privacy and security notices |
| AC.2.013 | 3.1.11 | Terminate sessions after defined conditions |
| AC.2.015 | 3.1.13 | Employ cryptographic mechanisms to protect CUI during transmission |
| AC.2.016 | 3.1.14 | Control CUI posted or processed on publicly accessible systems |
| AU.2.041 | 3.3.1 | Create and retain system audit logs |
| AU.2.042 | 3.3.2 | Ensure individual accountability |
| AU.3.045 | 3.3.5 | Correlate audit record review and analysis |
| AU.3.046 | 3.3.6 | Provide audit record reduction and report generation |
| CM.2.061 | 3.4.1 | Establish and maintain baseline configurations |
| CM.2.062 | 3.4.2 | Establish and enforce security configuration settings |
| CM.2.064 | 3.4.4 | Analyze security impact of changes prior to implementation |
| CM.2.065 | 3.4.5 | Define, document, approve, and enforce physical access restrictions |
| IA.1.076 | 3.5.1 | Identify system users and processes |
| IA.1.077 | 3.5.2 | Authenticate users, processes, and devices |
| IA.2.078 | 3.5.3 | Use multifactor authentication for local and network access to CUI |
| IA.2.079 | 3.5.4 | Employ replay-resistant authentication mechanisms |
| IA.2.081 | 3.5.7 | Enforce minimum password complexity and change requirements |
| IA.3.083 | 3.5.10 | Employ cryptographic mechanisms to protect authenticators |
| IR.2.092 | 3.6.1 | Establish operational incident-handling capability |
| IR.2.093 | 3.6.2 | Track, document, and report incidents |
| MA.2.111 | 3.7.1 | Perform maintenance on organizational systems |
| MA.2.112 | 3.7.2 | Provide controls on tools, techniques, and personnel used for maintenance |
| MP.1.118 | 3.8.1 | Protect system media containing CUI |
| MP.2.119 | 3.8.2 | Limit access to CUI on system media to authorized users |
| PE.1.131 | 3.10.1 | Limit physical access to systems to authorized individuals |
| PE.1.132 | 3.10.2 | Protect and monitor the physical facility and support infrastructure |
| RE.2.137 | 3.11.1 | Periodically assess risk to operations, assets, and individuals |
| RM.2.141 | 3.11.1 | Periodically assess the risk to organizational operations |
| RM.2.142 | 3.11.2 | Scan for vulnerabilities in systems periodically |
| RM.2.143 | 3.11.3 | Remediate vulnerabilities in accordance with assessments of risk |
| CA.2.157 | 3.12.1 | Periodically assess security controls to determine effectiveness |
| CA.2.158 | 3.12.2 | Develop and implement plans of action designed to correct deficiencies |
| CA.2.159 | 3.12.3 | Monitor security controls on an ongoing basis |
| SC.1.175 | 3.13.1 | Monitor, control, and protect communications at external boundaries |
| SC.2.179 | 3.13.7 | Prevent remote devices from simultaneously connecting (split tunneling) |
| SC.3.177 | 3.13.8 | Implement cryptographic mechanisms to prevent unauthorized disclosure |
| SI.1.210 | 3.14.1 | Identify, report, and correct system flaws in a timely manner |
| SI.1.211 | 3.14.2 | Provide protection from malicious code |
| SI.1.212 | 3.14.3 | Perform periodic scans and real-time scans of files from external sources |
| SI.2.214 | 3.14.6 | Monitor systems to detect attacks and indicators of potential attacks |
| SI.2.216 | 3.14.7 | Identify unauthorized use of systems |

## Source Domain Directory Mapping

When ingesting a document, use these indicators to determine the correct Sources/ subdirectory:

| Domain | Key Indicators |
|---|---|
| CMMC-Model | "CMMC", "Cybersecurity Maturity Model Certification", "CMMC 2.0", practice requirements |
| NIST-800-171 | "SP 800-171", "800-171", "NIST", "3.x.x control numbers" |
| NIST-800-172 | "SP 800-172", "800-172", "enhanced requirements", "Level 3" |
| Assessment-Guides | "CAP", "CAG", "assessment guide", "assessment process", "C3PAO", "assessment objectives" |
| DoD-Policy | "DFARS", "252.204", "DODI", "memo", "policy", "DAaaS", "CMMC-AB" |
| CUI-Categories | "CUI", "controlled unclassified information", "32 CFR 2002", "CUI registry" |
| Exam-Prep | "CCP", "CCA", "exam", "practice questions", "workbook", "study guide" |

## CUI Category Abbreviations

| Category | Abbreviation |
|---|---|
| Controlled Technical Information | CTI |
| Defense Critical Infrastructure Information | DCII |
| Export Controlled | EC |
| Naval Nuclear Propulsion Information | NNPI |
| Personally Identifiable Information | PII |
| Privacy | PRV |
| Proprietary Business Information | PBI |
| Technical Data | TD |
