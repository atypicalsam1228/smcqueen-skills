---
name: cyber-training-project
description: Generate a hands-on cybersecurity training project document (.docx) for a specific module. Follows a consistent scenario-based format matching the NetWatch/IronGate/CyberNova project style. Use when the user asks to create a training project, lab, or hands-on exercise for a cybersecurity module.
origin: learned
---

# Cybersecurity Training Project Generator

Creates hands-on project documents (.docx) for cybersecurity training modules. Each project
follows a consistent scenario-based format proven across 4 modules (Linux Admin, Linux Hardening,
Scripting, Networking).

## When to Activate

- User says "create a project for Module X.Y"
- User asks to "do the same for this module" with bullet-point topic list
- User provides a list of hands-on topics and wants a lab document
- User asks for a training exercise, lab, or hands-on project document

## Workflow

### Step 1 — Clarify Time Constraint
If the user has not specified a time limit, estimate it using this table and confirm before building:

| Scope | Estimate | Notes |
|-------|----------|-------|
| Single focused topic (e.g. SSH hardening) | 1.5–2 hrs | Narrow, one tool |
| 4–5 related topics, one VM | 2–2.5 hrs | Most single-module labs |
| 4–5 topics requiring multi-node lab | 3–3.5 hrs | Networking, containers |
| Full module with 6+ topics + integration | 3.5–4 hrs | Cross-cutting modules |

### Step 2 — Choose a Scenario Company
Rotate through these fictional company names for variety. Match the company theme to the module topic:

| Company | Theme | Good For |
|---------|-------|----------|
| CyberNova Solutions | MSSP / SOC operations | Scripting, monitoring, incident response |
| IronGate Infrastructure | Hosting / regulated clients | Hardening, compliance, GRC |
| NetWatch Labs | Cloud-native microservices | Networking, cloud, containers |
| FreshEats (from Terraform project) | SaaS / startup | IaC, CI/CD, DevSecOps |
| ShieldPoint Security | Consulting / pentesting | Threat modeling, red team, app security |
| DataVault Corp | Financial services / data | Cloud security, encryption, GRC |

### Step 3 — Write the Generator Script
Create a Python script at:
`C:\Users\samue\OneDrive\Desktop\Projects\cybersecurity_engineer_architect_training\generate_<topic>_project.py`

Use the boilerplate below, then add content sections. Run it to produce the .docx.

### Step 4 — Run and Deliver
```powershell
cd "C:\Users\samue\OneDrive\Desktop\Projects\cybersecurity_engineer_architect_training"
python generate_<topic>_project.py
```

Output goes to the same directory as `<Topic>-Project.docx`.

### Step 5 — Prompt for Markdown Companion File
After the .docx is generated, always ask the user:

> "Would you like me to also create a Markdown (.md) version with copyable code blocks?"

If yes, invoke the `docx-to-markdown` skill to convert the generated .docx into a .md file with all commands in fenced code blocks (PowerShell and Python tagged appropriately).

---

## Python Boilerplate (Copy This Exactly)

```python
"""
Generates the Module X.Y <Topic> hands-on project document.
Format mirrors: Bedrock Security Project, Terraform-IaC-Project, Secure-IaC-AI-Pipeline-Project.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# ── Style overrides ──────────────────────────────────────────────────
style = doc.styles['Title']
style.font.size = Pt(24)
style.font.color.rgb = RGBColor(0, 51, 102)

for level, size, color in [
    ('Heading 1', 18, RGBColor(0, 51, 102)),
    ('Heading 2', 14, RGBColor(0, 80, 140)),
    ('Heading 3', 12, RGBColor(0, 100, 160)),
]:
    s = doc.styles[level]
    s.font.size = Pt(size)
    s.font.color.rgb = color

# ── Helper functions ─────────────────────────────────────────────────

def add_title(text):
    doc.add_heading(text, level=0)

def h1(text):
    doc.add_heading(text, level=1)

def h2(text):
    doc.add_heading(text, level=2)

def h3(text):
    doc.add_heading(text, level=3)

def para(text):
    p = doc.add_paragraph(text)
    for r in p.runs:
        r.font.size = Pt(11)
    return p

def bullet(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    for r in p.runs:
        r.font.size = Pt(11)
    return p

def numbered(text):
    p = doc.add_paragraph(text, style='List Number')
    for r in p.runs:
        r.font.size = Pt(11)
    return p

def note(emoji, text):
    """Callout box. Use: '\U0001f4cc' (pin), '\U0001f512' (lock), '\U0001f4a1' (bulb)"""
    p = doc.add_paragraph()
    run = p.add_run(f'{emoji} ')
    run.font.size = Pt(11)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.italic = True
    return p

def code_block(lines):
    """Monospace indented code block. Pass a list of strings or a single string."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    text = '\n'.join(lines) if isinstance(lines, list) else lines
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(30, 30, 30)
    return p

def summary_list(items):
    """Bold 'Summary:' header followed by bullet points."""
    para('')
    p = doc.add_paragraph()
    run = p.add_run('Summary:')
    run.bold = True
    run.font.size = Pt(11)
    for item in items:
        bullet(item)

def add_table(headers, rows):
    """Light Grid Accent 1 table with bold headers."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
    for row_data in rows:
        row = table.add_row()
        for i, val in enumerate(row_data):
            row.cells[i].text = val
            for p in row.cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
    doc.add_paragraph('')
    return table

# =====================================================================
# DOCUMENT CONTENT — fill in below
# =====================================================================

add_title('Project Title Here')
para('Module X.Y — Subtitle Here')
para('')

# ... content sections ...

# =====================================================================
# SAVE
# =====================================================================
output_path = r'C:\Users\samue\OneDrive\Desktop\Projects\cybersecurity_engineer_architect_training\Output-Filename.docx'
doc.save(output_path)
print(f'Document saved to: {output_path}')
```

---

## Mandatory Document Structure

Every project document MUST include these sections in this order:

### 1. Project Overview (always first)
```
add_title('Project Title')
para('Module X.Y — Subtitle')

h1('Project Overview')
h2('Scenario')       # 2-3 sentence fictional company backstory
h2('Our Solution')   # What the student will build and why
h2('About the Project')  # bullet list: OS, Environment, Difficulty, Focus, Prerequisites
h2('Steps To Be Performed')  # numbered list of all major sections
h2('Tools & Technologies Used')  # add_table(['Tool / Technology', 'Purpose'], [...])
h2('Estimated Time & Cost')  # add_table with time, compute cost, cloud cost, software
h2('Architectural Diagram')  # ASCII art code_block showing the lab topology
h2('Final Result')   # What the student will have at the end
```

### 2. Numbered Content Sections
- Each major topic area becomes an `h1('N. Section Title')` section
- Each step within a section is `h2('Step N — Description')`
- Every section ends with `summary_list([...])` — 3–5 bullet points of what was learned
- Code blocks use realistic, runnable commands (not pseudocode)
- Every concept table uses `add_table()`
- Place `note()` callouts after complex commands or security-critical steps

### 3. Standard Closing Sections (always last, in this order)
```
h1('Cleanup')           # How to undo or reset the lab environment
h1('Best Practice Notes')  # Numbered list + reference table
h1('Project Complete')  # Summary of what was learned + bullet list of deliverables
                        # End with a note() pointing to the next module
```

---

## Note Callout Types

| Emoji | Unicode | Use For |
|-------|---------|---------|
| 📌 | `'\U0001f4cc'` | Explanatory notes, "how this works in production" |
| 🔒 | `'\U0001f512'` | Security warnings, critical steps, attack vectors |
| 💡 | `'\U0001f4a1'` | Tips, alternatives, career advice |

---

## Content Standards

### Default Command Language: PowerShell
- All shell commands in generated projects MUST default to **PowerShell** syntax, not Linux/bash
- Use PowerShell equivalents for all operations:
  - `cat > file << 'EOF'` → `@" ... "@ | Out-File -Encoding utf8 file`
  - `mkdir -p` → `New-Item -ItemType Directory -Force -Path`
  - `chmod 444` → `Set-ItemProperty -Name IsReadOnly -Value $true`
  - `curl` → `Invoke-RestMethod`
  - `ls -lh` → `dir` or `Get-ChildItem`
  - `sha256sum` → `Get-FileHash -Algorithm SHA256`
  - `python3` → `python`
  - `pip install` → `python -m pip install`
  - `export VAR=value` → `$env:VAR = "value"`
  - `cat file` → `Get-Content file`
  - `pkill -f` → `Stop-Process -Name`
- If a Linux-specific command has no PowerShell equivalent (e.g., systemctl, apt), note that it requires WSL or a Linux VM

### Default Coding Language: Python
- All coding examples and scripts MUST default to **Python** unless the topic specifically requires another language
- If the original topic involves another language (e.g., Bash scripting, Go), provide the Python equivalent alongside it
- Use idiomatic Python (PEP 8 style, standard library where possible)

### Code Blocks
- Always use realistic commands the student can actually run on Windows/PowerShell
- Include comments (`#`) explaining what each command does
- Show expected output when it helps understanding
- Use `@" ... "@ | Out-File` for multi-line file creation (not heredocs)
- Tag PowerShell commands appropriately in the document

### Tables
- Every major concept comparison gets a table (not a bullet list)
- Column count: 2–5 columns max for readability
- Common table patterns used across all projects:
  - `['Tool / Technology', 'Purpose']` — services used
  - `['Concept', 'Description', 'Security Implication']` — concept reference
  - `['CIS Control', 'Setting', 'Value', 'Security Impact']` — compliance mapping
  - `['Item', 'Detail']` — time/cost estimates

### Scenario Narrative Rules
- 2–3 sentences max for the Scenario
- The fictional company has a real problem (outage, audit finding, compliance gap, breach)
- The student is a specific role (Junior Security Engineer, Security Engineer, new hire)
- The manager has given a specific task

### Backward Compatibility Note in "Project Complete"
- Always end the last `note()` with: "Next module: Module X.Y — [Name]. [One sentence connecting this module's skills to the next.]"

---

## Completed Projects Reference

| File | Module | Topic | Time | Company |
|------|--------|-------|------|---------|
| `Linux-Systems-Admin-Fundamentals-Project.docx` | 1.1 | Linux Admin (filesystem, users, packages, systemd, cron, logs) | 2 hrs | NovaTech |
| `Linux-Hardening-CIS-Compliance-Project.docx` | 1.2 | CIS Benchmarks, SSH hardening, SUID audit, AppArmor, unattended-upgrades | 2.5 hrs | IronGate Infrastructure |
| `Scripting-Languages-Security-Automation-Project.docx` | 1.3 | Bash, Python (requests/yaml/subprocess/json), PowerShell, cron automation | 3 hrs | CyberNova Solutions |
| `Networking-Core-Concepts-Project.docx` | 2.1 | OSI, Wireshark, bind9, subnetting, NAT/DHCP, Nginx L7, HAProxy L4, NTP/chrony | 3.5 hrs | NetWatch Labs |

All generator scripts are saved alongside the .docx files in:
`C:\Users\samue\OneDrive\Desktop\Projects\cybersecurity_engineer_architect_training\`

---

## Encoding & Known Issues

- Always include `sys.stdout.reconfigure(encoding='utf-8')` at the top of every generator script
- Use Unicode escapes for special characters in string literals: `\u2014` (—), `\u2022` (•)
- Regex patterns inside code_block strings: use raw-style notation in comments only; the actual content is just a string being written to a file, not executed by Python
- If python-docx raises `PackageNotFoundError` on a source .docx, copy it to a temp location first before reading
- Run scripts with: `python generate_<topic>_project.py` (not `python3`) on this Windows machine

---

## Training Curriculum Context

The full 10-phase training protocol is at:
`C:\Users\samue\OneDrive\Desktop\Projects\cybersecurity_engineer_architect_training\TRAINING_PROTOCOL.md`

Phase ordering (each phase builds on the prior):
1. Linux & Scripting (Modules 1.1, 1.2, 1.3)
2. Networking (Module 2.1)
3. Cloud Security
4. Infrastructure as Code
5. Containers & Kubernetes
6. CI/CD & DevSecOps
7. API & Application Security
8. Monitoring & Incident Response
9. Threat Modeling
10. GRC & Leadership
