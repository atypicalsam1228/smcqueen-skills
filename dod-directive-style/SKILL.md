# DoD Policy Generator

Generate formal policy and procedural documents in the DoD Instruction (DoDI) format. This skill enforces the structural conventions, writing register, and formatting rules derived directly from authoritative DoD issuances such as DoDI 8531.01.

Use this skill whenever the user asks to:
- Draft a policy document, plan, or directive
- Write in formal government/regulatory style
- Produce a document that will be submitted as part of a compliance package (FedRAMP, RMF, CMMC, etc.)
- Rewrite an existing document into DoD Instruction format

---

## Activation

When this skill is invoked, ask the user for the following before writing anything:

```
To generate a DoD-style policy document I need:

1. Document title (e.g., "Vulnerability Management Plan")
2. Originating organization / company name
3. Subject matter — what program, process, or policy does this govern?
4. Roles — list the key roles that will appear in the Responsibilities section
5. Placeholders or real names? (use [COMPANY NAME] etc., or fill in actuals)
6. Output format(s):
      A — Markdown only
      B — Word, annotated (control references after each section)
      C — Word, clean corporate (no annotations)
      A + B — Markdown and annotated Word
      A + C — Markdown and clean Word
      B + C — Both Word versions
      All three

Provide these and I will produce the full document.
```

Do not begin writing until all six are provided.

---

## Document Structure (Always Use This Order)

Every document produced by this skill follows this exact sequence:

```
1. Cover Block
2. Table of Contents
3. Section 1: General Issuance Information
   1.1 Applicability
   1.2 Policy
   1.3 Relationship to Other Documents  ← include when relevant
4. Section 2: Responsibilities
   2.1 [Role 1]
   2.2 [Role 2]
   ... one subsection per role
5. Section 3+: Process / Procedures
   (one section per major process phase)
6. Glossary
   G.1 Acronyms
   G.2 Definitions
7. References
```

Never collapse or reorder these sections. A reader familiar with DoDI format must be able to navigate the document without orientation.

---

## Cover Block

The cover block appears before the Table of Contents and contains these fields, left-aligned, bold label followed by value:

```
[ORGANIZATION NAME]
[DOCUMENT TITLE]                          ← centered, largest font

Document Identifier:    [ORG-ABBREV]-[TYPE]-[NUMBER]
System Name:            [SYSTEM NAME]
Originating Component:  [ORGANIZATION] — [Office Name]
Effective Date:         [DATE]
Review Cycle:           Annual, or following any significant change
Document Classification: Controlled Unclassified Information (CUI)
Approved by:            [NAME], [TITLE]

Purpose:  [3–5 bullet points stating what the document establishes]
```

The Purpose bullets each begin with a gerund verb: "Establishes...", "Assigns...", "Provides...".

---

## Writing Register

### The Cardinal Rule

Every obligation is written in active imperative voice with a named subject:

```
CORRECT:  The ISSO will review all vulnerability scan results within three (3) business days.
WRONG:    Scan results should be reviewed in a timely manner.
WRONG:    Vulnerability scans are to be reviewed by security personnel.
WRONG:    It is required that scan results be reviewed.
```

There is no passive voice in obligations. Passive voice is only acceptable in definitions and background statements.

### Role Introduction Pattern

Every Responsibilities subsection opens with the role name as subject:

```
The System Owner:
The ISSO:
The Vulnerability Management Team:
```

For subordinate roles, use the authority framing before the colon:

```
Under the authority and direction of the [Superior Role], the [Subordinate Role]:
Under the authority, direction, and control of the [Superior], and in addition to
the responsibilities in Paragraph X.X., the [Role]:
```

The phrase "in addition to the responsibilities in Paragraph X.X." is used whenever a role inherits duties from a parent section.

### Two-Mode Obligation System

DoD Instructions use two distinct verb registers depending on where in the document the obligation appears. Use the wrong mode in the wrong section and the document reads as inconsistent.

**Section 2 — Responsibilities mode (role-level duties):**
Use gerund present-tense verbs as the first word of each lettered item, with the role name as the implied subject established by the section opener:

| Verb | When to use |
|---|---|
| **Establishes** | Creating a policy, program, process, or governance body |
| **Coordinates** | Action requires working with another party |
| **Maintains** | Ongoing stewardship of a resource, system, or program |
| **Approves / Denies** | Decision authority |
| **Designates** | Appointing a person or office to a role |
| **Ensures** | Oversight duty — confirms something happens, may delegate the doing |
| **Provides** | Delivering guidance, support, or a service |
| **Develops** | Creating new policy, standards, or capabilities |
| **Identifies** | Finding, naming, or cataloguing something |

Example:
```
The ISSO:
a.  Coordinates the scheduling and execution of all vulnerability scans.
b.  Maintains all scan reports and deviation records.
c.  Approves or denies deviation requests from operations personnel.
```

**Sections 3+ — Implementation mode (technical/procedural mandates):**
Use `must` with a named subject for all technical requirements. `must` signals a non-discretionary implementation obligation at the system or process level:

```
System owners must implement authenticated scans monthly.
IT resource owners must define and document authorization requirements.
Attribute services must register relying parties before providing attributes.
```

The shift from gerund (Section 2) to `must` (Section 3+) is intentional — it signals a change of register from who-owns-what to what-must-be-done. Both modes are correct in their respective contexts.

**`will` usage:**
Reserve `will` for organization-level policy commitments in Section 1.2, and for forward-looking statements in process sections where the actor is the organization as a whole:
```
[ORGANIZATION] will conduct an annual penetration test.  ← Section 1.2 policy item
[ORGANIZATION] will retain all ConMon packages for three years.  ← process section org-level
```

**Banned soft language (all sections):**
Never use: *should*, *may wish to*, *is encouraged to*, *strives to*, *aims to*.

**Exception — `should` for explicit recommendations:**
`should` is permitted only when the document is consciously contrasting a recommendation against a nearby mandate, where the distinction is operationally meaningful (e.g., a migration timeline where Components have discretion over method but not outcome). When used, it must appear alongside a mandatory counterpart so the reader can see the distinction:
```
System owners must provision entitlements using explicit access.
System owners should adopt automated provisioning tools by [DATE].  ← recommendation, not mandate
```
Do not use `should` in isolation as a softened mandate. If the action is required, use `must` or `will`.

---

## Item Formatting

### Parallel vs. Sequential Items — Choose the Right Format

This is the most common structural mistake in DoD-style documents. The format signals the relationship between items:

**Lettered items (a. b. c.) = parallel, independent duties.**
Use when items can be read in any order and none depends on a prior item completing first. Section 2 Responsibilities always uses lettered items.

```
a.  Conducts monthly vulnerability scans.
b.  Reviews scan results within two business days.
c.  Maintains deviation documentation for three years.
```

**Numbered items (1. 2. 3.) = sequential steps in a workflow.**
Use when order matters — step 2 cannot begin until step 1 is complete. Approval processes, incident response procedures, and provisioning workflows always use numbered items:

```
1.  The sponsor compiles the required attribute service information.
2.  The sponsor submits the package to the DoD CIO ICAM lead.
3.  The DoD CIO ICAM lead coordinates a governance review.
4.  If approved, the DoD CIO signs the approval memorandum.
```

**Counter-example to avoid:** Using lettered items (a. b. c.) for a sequential approval process implies the steps are interchangeable — they are not, and a reader can be misled about execution order.

---

### Lettered Sub-items (first level under a role or section)

```
a.  First duty or requirement.
b.  Second duty or requirement.
c.  Third duty or requirement.
```

Two spaces after the letter-period. Sentence case. Period at end.

### Numbered Sub-sub-items (second level)

```
a.  Parent item text:

    (1)  First sub-item.
    (2)  Second sub-item.
    (3)  Third sub-item.
```

Indented under the parent. Parenthetical number, two spaces, text.

### Third level (rare — use only when unavoidable)

```
    (2)  Second sub-item:

         (a)  First nested item.
         (b)  Second nested item.
```

Do not go deeper than three levels. If content requires more nesting, restructure into a separate subsection.

**Deep nesting is a sign that content should be a table.** When de-provisioning timelines, SLA thresholds, or decision matrices reach level 3+, convert to a table instead. Five-level nesting (observed in DoDI 8520.04 Section 4.2) is always a restructuring failure — a table with columns for Event Type, Access Type, and Timeline would have conveyed the same information in half the space with zero nesting.

### Tables

Use a table when presenting:
- Multi-column reference data (SLAs, severity ratings, role mappings, tool inventories)
- Comparison or decision criteria
- Structured lists with 3+ attributes per item

Do not use a table for simple single-column lists — use lettered items instead.

Every table gets:
- A bold title above it: `Table N. [Descriptive Title]`
- A shaded or bold header row
- Consistent column widths appropriate to content length

---

## Section 1 Conventions

### 1.1 Applicability

One paragraph. Names every organizational entity the document governs. Uses the phrase "referred to collectively in this issuance as the '[SHORT NAME]'" to establish the shorthand used throughout:

```
This plan applies to all personnel, systems, subsystems, and system components
within the [SYSTEM NAME] authorization boundary... Contractors and subcontractors
with access to [SYSTEM NAME] components are subject to the requirements of this plan.
```

### 1.2 Policy

Opens with "[ORGANIZATION] will:" followed by lettered items (a. b. c.). Each item is one concrete, enforceable obligation. This is the highest-level statement of what the organization is committing to do — not how.

Keep each policy item to one sentence. No sub-items under policy items. Save the "how" for Section 3.

### 1.3 Relationship to Other Documents

A simple table mapping related documents to their relationship to this one:

| Document | Relationship |
|---|---|
| System Security Plan | Parent document; defines boundary |
| Configuration Management Plan | Governs change control procedures |

---

## Section 2 — Responsibilities Conventions

- One subsection (2.1, 2.2, ...) per role in descending order of authority
- The most senior role appears first
- Each subsection is entirely self-contained — do not split one role's duties across subsections
- Where a role has 10+ duties, consider grouping related duties under a brief unnumbered heading within the subsection, but keep the lettered-item format throughout
- Roles are always referred to by title, never by name of the current incumbent
- Use acronyms consistently once defined: first use is "Information System Security Officer (ISSO)", all subsequent uses are "ISSO"

---

## Section 3+ — Process / Procedure Conventions

### Step Labeling

Multi-step processes use the format:

```
3.2.  STEP 1: [STEP NAME IN ALL CAPS].
3.3.  STEP 2: [STEP NAME IN ALL CAPS].
```

### General Subsection

If the process section has more than two steps, open with a `[X].1. GENERAL.` subsection that describes the process as a whole in one paragraph before the steps begin.

### Process Item Voice

Process steps use the same "[ORGANIZATION] will:" or "[ROLE] will:" structure as responsibilities. Never use "the system" or "the process" as the subject — a human role is always the actor.

### Tables in Process Sections

Numerical thresholds, schedules, and SLAs always go in a table, not in prose. A reader enforcing compliance must be able to find the number instantly:

```
Table 3. Remediation SLAs
| CVSS Score | Severity | SLA       |
| 9.0–10.0   | Critical | 30 days   |
```

---

## Glossary Conventions

### G.1 Acronyms

A two-column table: Acronym | Meaning. Alphabetical order. Include every acronym used in the document body.

### G.2 Definitions

Opens with: *"Unless otherwise noted, these terms and definitions apply to this [plan / issuance / instruction]."*

A two-column table: Term | Definition. Alphabetical order.

Definition style:
- Noun phrase followed by definition, no subject-verb construction
- If defined elsewhere, write: `Defined in [SOURCE DOCUMENT].` — do not restate the definition
- If defined specifically for this document, write the full definition
- Do not use the term being defined in its own definition

Example:
```
| remediation | The elimination or correction of a vulnerability, typically through
               the application of a vendor-supplied patch, configuration change,
               or software update. |
| mitigation  | Defined in CNSSI 4009. |
```

---

## References Section

Final section. No section number — just the heading "REFERENCES".

List format: one entry per line, no bullets, alphabetical by organization name. Full citation:

```
[Organization], "[Document Title]," [Date/Edition]
National Institute of Standards and Technology Special Publication 800-53,
Revision 5, "Security and Privacy Controls for Information Systems and
Organizations," September 2020
```

Always include:
- All NIST SPs and IRs cited
- All CNSSI instructions cited
- All DoD Directives and Instructions cited
- The parent SSP, CMP, IRP, and ConMon Strategy (as internal references with placeholders)

---

## Cross-Reference Language

When referring to another part of the document:

```
in accordance with Paragraph 3.4          ← within same section
as defined in Section 2                   ← section-level reference
in accordance with the requirements in    ← general forward reference
  Paragraphs 3.4 through 4 of this plan
per Table 3                               ← table reference
```

Never use "see above" or "see below" — always give the specific section/paragraph number.

---

## Common Errors to Avoid

| Error | Correction |
|---|---|
| Passive obligation: "Scans are to be performed monthly" | Active: "The Vulnerability Management Team will perform scans monthly" |
| Vague timing: "in a timely manner" | Specific: "within five (5) business days" |
| Soft obligation: "should maintain an inventory" | Hard: "will maintain an inventory" |
| Unnamed actor: "It is required that..." | Named actor: "The ISSO will..." |
| Typo in section header | Review all headers — capitalize consistently, spell out acronyms on first use |
| Internal link says "see below" | Replace with "in accordance with Section X.X" |
| Acronym used before defined | Define at first use: "Information System Security Officer (ISSO)" |
| Nested list deeper than 3 levels | Restructure as a separate subsection or convert to a table |
| Policy item contains "how" | Move "how" to Section 3; policy states "what" only |
| Definitions section missing "Unless otherwise noted..." opener | Always include this opener |
| Mixed verb forms in one role's subsection: "Establishes..., Identifying..." | All items in a single subsection must use the same grammatical form |
| Sequential workflow using lettered items (a. b. c.) | Sequential steps must use numbered items (1. 2. 3.) |
| `should` used as a standalone softened mandate | Pair with a nearby `must` or rewrite as `must` — `should` alone is not policy language |
| Informal language: "please contact", "note that", "keep in mind" | Remove — DoD Instructions do not use conversational register |
| Definitional statement placed in a Protocols or Procedures section | Move to G.2 Definitions |

---

## Document Footer

Every page footer (or final line of document if producing markdown):

```
[ORGANIZATION NAME] — [SYSTEM NAME] [DOCUMENT TITLE] — [DOCUMENT IDENTIFIER]
Controlled Unclassified Information (CUI) — Do not distribute without authorization
```

---

## Output Format

Three output modes are supported. The user specifies which format(s) to produce. If the user does not specify, default to Markdown. When multiple formats are requested, generate them all.

---

### Format A — Markdown (.md)

1. Produce the full document in markdown using `##` for section headings, `###` for subsections
2. Use `**bold**` for table headers and label fields in the cover block
3. Use standard markdown tables for all tabular data
4. Indent sub-items using consistent 4-space indentation in prose sections
5. Insert a horizontal rule (`---`) between major sections
6. No control annotations unless the user explicitly requests them in the markdown output

---

### Format B — Word (.docx), Annotated (with control references)

Generate a Python script using `python-docx` that produces a `.docx` file. Do not convert markdown to Word directly.

**Purpose:** Internal compliance team use, ATO package submissions, auditor review. Each section closes with a clearly marked control reference block so the reader can trace every policy statement back to a NIST 800-53 or framework control.

**Control reference block rules:**

- Append a control reference block **after the closing paragraph of each numbered section** (Section 1, Section 2, each Section 3+ subsection)
- Format the block as a shaded paragraph (light gray, hex `D9D9D9`) with the label **"Applicable Controls:"** in bold, followed by the control IDs and short titles in a single line
- Use the format: `RA-5 (Vulnerability Scanning), SI-2 (Flaw Remediation), CA-7 (Continuous Monitoring)`
- Map controls to sections based on subject matter — do not paste the same generic list on every section. Examples:

| Section Subject | Controls to Cite |
|---|---|
| Scanning / vulnerability identification | RA-5, SI-2 |
| Continuous monitoring / ConMon | CA-7, RA-5 |
| Remediation timelines / POA&M | SI-2, CA-5 |
| Penetration testing | CA-8 |
| Asset inventory | CM-8 |
| Responsibilities / roles | PM-2, CA-7 |
| Access and authorization | AC-2, AC-6 |
| Incident handling | IR-4, IR-5 |
| Configuration management | CM-6, CM-7 |
| Supply chain / vendor | SR-3, SR-5 |

- If the document targets FedRAMP Moderate, cite both the NIST control ID and the FedRAMP-specific parameter where one exists (e.g., `RA-5 (FedRAMP Moderate: monthly authenticated scans)`)
- If no NIST control maps cleanly, omit the block rather than inventing a mapping

**python-docx implementation for control reference block:**

```python
def add_control_ref(doc, controls_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    # Light gray shading
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'D9D9D9')
    pPr.append(shd)
    run_label = p.add_run('Applicable Controls: ')
    run_label.bold = True
    run_label.font.size = Pt(10)
    run_controls = p.add_run(controls_text)
    run_controls.font.size = Pt(10)
    run_controls.italic = True
```

**Other python-docx conventions (both Word versions):**

- Font: Times New Roman 12pt body, 11pt table cells, 10pt control reference blocks
- Margins: 1.25" left/right, 1.0" top/bottom
- Section headings: Bold, 12pt, all caps for major section titles (SECTION 1, SECTION 2)
- Subsection headings: Bold, 12pt, mixed case (1.1 Applicability)
- Lettered items: 0.5" left indent, hanging indent to align text after `a.  `
- Table header rows: shaded `4472C4` (dark blue) with white bold text, or `D9D9D9` with black bold text depending on table prominence
- Column widths: set explicitly in `Inches()` — never rely on Word auto-sizing
- Cover block: centered org name and document title; all other fields left-aligned with bold label

---

### Format C — Word (.docx), Clean Corporate (no control references)

Generate a second Python script (or a flag/parameter in the same script) that produces a `.docx` identical to Format B **except:**

- No control reference blocks anywhere in the document
- The document reads as a standalone corporate policy — no compliance jargon visible to a non-technical reader unless it is part of the policy language itself
- Acronyms like NIST, FedRAMP, CVSS may still appear in the body where they are operationally relevant, but the shaded annotation blocks are absent
- Suitable for distribution to all-hands, HR onboarding, vendor sharing, or leadership review

**Implementation:** In the python-docx script, implement the clean version as a boolean flag at the top:

```python
ANNOTATED = False   # Set True for Format B (with control references), False for Format C (clean)
```

The `add_control_ref()` function becomes a no-op when `ANNOTATED = False`:

```python
def add_control_ref(doc, controls_text):
    if not ANNOTATED:
        return
    # ... shading logic ...
```

This ensures both versions are produced from a single script with a one-line change, reducing maintenance overhead.

---

### Requesting output formats

When the user asks to "save as Word" without specifying annotated or clean, ask:

```
Which Word version would you like?
  B — Annotated (control references after each section, for compliance/audit use)
  C — Clean corporate (no annotations, reads as standard policy)
  Both
```

When the user asks for "both Word versions," generate one Python script with the `ANNOTATED` flag and instruct the user to run it twice — once with `ANNOTATED = True`, once with `ANNOTATED = False` — producing two separate output files named:

```
[DocumentTitle]_Annotated.docx
[DocumentTitle]_Corporate.docx
```

---

## Quality Gate

Before delivering any document, verify:

- [ ] Every obligation has a named human role as subject
- [ ] No passive voice in obligation statements
- [ ] All timing language is specific (days/hours, not "timely" or "promptly")
- [ ] All acronyms defined on first use and collected in G.1
- [ ] All numerical thresholds are in a table, not buried in prose
- [ ] Cross-references use section/paragraph numbers, not "above/below"
- [ ] Glossary opens with "Unless otherwise noted..."
- [ ] References section is alphabetical and complete
- [ ] Cover block includes all required fields
- [ ] Section 2 items all use the same grammatical form (all gerunds: "Establishes...", "Coordinates..." — not a mix of gerunds and participles)
- [ ] Sequential workflows use numbered items; parallel duties use lettered items
- [ ] No `should` in isolation — every `should` is paired with a nearby `must` to make the recommendation/mandate distinction explicit
- [ ] No deep nesting past level 3 — if level 4+ appears, convert to a table
- [ ] No informal language ("please contact", "note that", "keep in mind") anywhere in the body

---

## Word Document Format Checklist

Run this checklist against every generated `.docx` before delivery. This checklist enforces the DoD Instruction formatting standard derived from the Vulnerability Management Plan (VMP) as the master reference document.

### Page Setup
- [ ] Page size: 8.5" × 11" (Letter)
- [ ] Top margin: 1.0"
- [ ] Bottom margin: 1.0"
- [ ] Left margin: 1.25"
- [ ] Right margin: 1.25"

### Cover Block Formatting
- [ ] Organization name: Times New Roman, 18pt, Bold
- [ ] Document title: Times New Roman, 16pt, Bold, centered or left-aligned consistently
- [ ] Cover metadata fields (Document Identifier, System Name, etc.): Times New Roman, 12pt
- [ ] Cover field labels (e.g., "Document Identifier:"): Bold
- [ ] Cover field values: Normal weight (not bold)
- [ ] Cover block uses Normal paragraph style — not a Heading style
- [ ] Blank line separates org name / title block from metadata fields

### Heading Styles
- [ ] Heading 1: 14pt, Bold, color `#365F91` (Steel Blue), space-before 24pt, space-after 0pt
- [ ] Heading 2: 13pt, Bold, color `#4F81BD` (Light Blue), space-before 10pt, space-after 0pt
- [ ] Heading 3 (if present): Bold, color `#4F81BD`, space-before 10pt, space-after 0pt
- [ ] No heading uses a color outside the approved palette (`#365F91`, `#4F81BD`)
- [ ] Heading styles applied via Word style — not manually formatted runs

### Body Text
- [ ] Body paragraphs use Normal paragraph style
- [ ] Body font: Times New Roman, 12pt (set at style level or run level consistently)
- [ ] No inline bold/italic on body text except for defined label patterns
- [ ] Line spacing: single or 1.15 — consistent throughout
- [ ] Space-after on body paragraphs: 6pt or 0pt — consistent throughout

### Tables
- [ ] Every table has a bold title above it: `Table N. Descriptive Title`
- [ ] Header row is shaded (`#4472C4` dark blue with white bold text, or `#D9D9D9` gray with black bold text)
- [ ] Column widths set explicitly in `Inches()` — no auto-sizing
- [ ] Table font: Times New Roman, 11pt in cells
- [ ] No table extends beyond page margins

### Control Reference Blocks (Annotated version only)
- [ ] Control ref blocks present after each major section in the annotated version
- [ ] Control ref blocks use shaded background `#D9D9D9`
- [ ] Label "Applicable Controls:" is bold, 10pt
- [ ] Control IDs are italic, 10pt
- [ ] Control ref blocks are entirely absent in the corporate/clean version
- [ ] Control ref blocks are entirely absent in the client-branded version

### Version-Specific Checks
- [ ] **Placeholder version**: all org/company fields use bracketed placeholders (`[COMPANY NAME]`, `[ORG]`, etc.)
- [ ] **With-controls version**: identical to placeholder version plus control ref blocks after each section
- [ ] **Client-branded version**: all placeholders replaced with the client organization name as appropriate; no control ref blocks; reads as clean corporate document

### Grammar and Typo Check
- [ ] All section headings spell-checked and consistently capitalized
- [ ] No double spaces in body text
- [ ] No orphaned brackets `[` or `]` from incomplete placeholder substitution
- [ ] Acronyms used in body match entries in G.1 Acronyms table exactly
- [ ] Numbered lists are sequential with no gaps (1, 2, 3 — not 1, 3, 4)
- [ ] Lettered lists are sequential with no gaps (a, b, c — not a, c, d)
- [ ] No sentence ends without a period
- [ ] Table cells do not contain trailing whitespace that breaks alignment

### Python-docx Script Verification
- [ ] Script runs without errors from command line: `python generate_[policy].py`
- [ ] Output file is a valid `.docx` (opens in Word without repair prompt)
- [ ] `ANNOTATED = True` produces the with-controls version
- [ ] `ANNOTATED = False` produces the clean/corporate version
- [ ] Client-branded version uses a separate flag or separate script call
- [ ] All three output files are written to the configured output directory
