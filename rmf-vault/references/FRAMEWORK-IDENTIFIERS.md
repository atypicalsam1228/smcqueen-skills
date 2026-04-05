# Framework Identifiers — Quick Reference

Use these identifier formats when referencing controls, requirements, and subcategories across frameworks.

## NIST 800-53 Rev 5

**Format:** `<Family>-<Number>` with optional enhancement `(<Enhancement>)`

| Family ID | Family Name | Example |
|---|---|---|
| AC | Access Control | AC-2, AC-6(1) |
| AU | Audit and Accountability | AU-2, AU-6(1) |
| AT | Awareness and Training | AT-2, AT-3 |
| CM | Configuration Management | CM-2, CM-7(1) |
| CP | Contingency Planning | CP-2, CP-9 |
| IA | Identification and Authentication | IA-2(1), IA-5(1) |
| IR | Incident Response | IR-4, IR-6 |
| MA | Maintenance | MA-2, MA-5 |
| MP | Media Protection | MP-2, MP-6 |
| PE | Physical and Environmental Protection | PE-2, PE-6 |
| PL | Planning | PL-2, PL-4 |
| PM | Program Management | PM-1, PM-9 |
| PS | Personnel Security | PS-3, PS-6 |
| PT | PII Processing and Transparency | PT-2, PT-3 |
| RA | Risk Assessment | RA-3, RA-5 |
| SA | System and Services Acquisition | SA-4, SA-11 |
| SC | System and Communications Protection | SC-7, SC-13 |
| SI | System and Information Integrity | SI-2, SI-4 |
| SR | Supply Chain Risk Management | SR-2, SR-3 |

**Linking pattern:**
```markdown
[[Sources/NIST-800-53/AC-access-control#AC-2 Account Management|AC-2]]
```

## FedRAMP

**Baselines:** Low, Moderate, High

FedRAMP uses NIST 800-53 controls with additional parameters and requirements. Reference by baseline + control:

```
FedRAMP Moderate AC-2
FedRAMP High SC-7(7)
```

**Linking pattern:**
```markdown
[[Sources/FedRAMP/fedramp-moderate-baseline#AC-2|FedRAMP Moderate AC-2]]
```

## NIST 800-171 Rev 2

**Format:** `3.<Family>.<Number>`

| Range | Family | 800-53 Mapping |
|---|---|---|
| 3.1.x | Access Control | AC family |
| 3.2.x | Awareness and Training | AT family |
| 3.3.x | Audit and Accountability | AU family |
| 3.4.x | Configuration Management | CM family |
| 3.5.x | Identification and Authentication | IA family |
| 3.6.x | Incident Response | IR family |
| 3.7.x | Maintenance | MA family |
| 3.8.x | Media Protection | MP family |
| 3.9.x | Personnel Security | PS family |
| 3.10.x | Physical Protection | PE family |
| 3.11.x | Risk Assessment | RA family |
| 3.12.x | Security Assessment | CA family |
| 3.13.x | System and Communications Protection | SC family |
| 3.14.x | System and Information Integrity | SI family |

**Total:** 110 requirements (29 Basic, 81 Derived)

**Linking pattern:**
```markdown
[[Sources/NIST-800-171/security-requirement-families#3.1.5|800-171 3.1.5]]
```

## NIST AI RMF 1.0

**Format:** `<Function>-<Number>.<Subcategory>`

| Function | ID Prefix | Subcategories |
|---|---|---|
| Govern | GV | GV-1 through GV-6 |
| Map | MP | MP-1 through MP-5 |
| Measure | MS | MS-1 through MS-4 |
| Manage | MG | MG-1 through MG-4 |

**Example:** `GV-1.1`, `MP-2.3`, `MS-3.2`, `MG-4.1`

**Linking pattern:**
```markdown
[[Sources/NIST-AI-RMF/govern-function#GV-1|AI RMF GV-1]]
```

## OWASP LLM Top 10 (2025)

**Format:** `LLM<Number>`

| ID | Risk |
|---|---|
| LLM01 | Prompt Injection |
| LLM02 | Sensitive Information Disclosure |
| LLM03 | Supply Chain Vulnerabilities |
| LLM04 | Data and Model Poisoning |
| LLM05 | Improper Output Handling |
| LLM06 | Excessive Agency |
| LLM07 | System Prompt Leakage |
| LLM08 | Vector and Embedding Weaknesses |
| LLM09 | Misinformation |
| LLM10 | Unbounded Consumption |

**Linking pattern:**
```markdown
[[Sources/OWASP-LLM/LLM01-prompt-injection|LLM01 Prompt Injection]]
```

## Cross-Framework Quick Lookup

When a user mentions a control, determine the framework by pattern:

| Pattern | Framework |
|---|---|
| `AC-2`, `SI-4(5)` | NIST 800-53 |
| `3.1.5`, `3.13.8` | NIST 800-171 |
| `FedRAMP Low/Moderate/High` + control | FedRAMP |
| `GV-1`, `MP-2.3`, `MS-1`, `MG-4` | NIST AI RMF |
| `LLM01`–`LLM10` | OWASP LLM Top 10 |
