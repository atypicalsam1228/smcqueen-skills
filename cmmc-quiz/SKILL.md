---
name: cmmc-quiz
description: "Pre-configured instance of /quiz-creator for the CMMC-AB Certified CMMC Professional (CCP) exam. All paths, domains, 6-domain blueprint (170 questions, 117 skills) are pre-set. Use for generating CCP practice questions, running gap analysis, and launching the local quiz app."
---

# CCP Quiz Manager

Pre-configured instance of the `/quiz-creator` skill for the **CMMC-AB Certified CMMC Professional (CCP)** exam. All paths, domains, and the 117-skill coverage map are already set up.

For the general-purpose quiz creation workflow, see `/quiz-creator`.

## Configuration (Pre-Set)

```
EXAM_NAME: CMMC-AB Certified CMMC Professional (CCP) v7.4
QUIZ_DIR: C:/Users/samue/repos/cmmc-quiz
VAULT_PATH: C:/Users/samue/OneDrive/Obsidian/CMMC_Vault
GENERATED_DIR: C:/Users/samue/OneDrive/Obsidian/CMMC_Vault/CCP-Exam/Sources/Generated-Questions
SOURCE_DIR: C:/Users/samue/OneDrive/Obsidian/CMMC_Vault/CCP-Exam/Sources
EXAM_GUIDE_PATH: C:/Users/samue/OneDrive/Obsidian/CMMC_Vault/CCP-Exam/Sources/ccp-exam-blueprint-v7-4.md
GIT_CMD: git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault
```

## Subcommands

| Command | Description |
|---------|-------------|
| `/cmmc-quiz status` | Show question counts, domain distribution, coverage % |
| `/cmmc-quiz generate <domain\|all> [count]` | Generate new CCP questions for a domain (1-6) |
| `/cmmc-quiz gap-analysis` | Compare questions against all 117 blueprint skills |
| `/cmmc-quiz gap-fill [count]` | Generate questions for uncovered skills |
| `/cmmc-quiz launch` | Kill existing server, start quiz at localhost:8765 |
| `/cmmc-quiz build` | Build or rebuild the quiz app |
| `/cmmc-quiz deploy` | Export questions and deploy to Vercel (live at cmmc-quiz.vercel.app) |
| `/cmmc-quiz` (no args) | Show subcommands |

All subcommands follow the workflows defined in `/quiz-creator` SKILL.md — this skill pre-fills the configuration.

## /cmmc-quiz deploy

Exports questions and deploys to Vercel. See **`quiz-static-deploy`** skill for the full pattern.

```bash
cd C:/Users/samue/repos/cmmc-quiz
python export_questions.py && npx vercel --prod
```

**Live URL**: https://cmmc-quiz.vercel.app
**iPhone**: Safari → URL → Share → Add to Home Screen

## Current Stats

| Domain | Weight | Est. Questions | Tasks | Skills |
|--------|--------|----------------|-------|--------|
| D1: CMMC Ecosystem | 5% | ~9 | 1 | 15 |
| D2: Ethics / CoPC | 5% | ~9 | 1 | 13 |
| D3: Governance & Source Documents | 15% | ~26 | 3 | 26 |
| D4: Model Construct & Implementation | 35% | ~60 | 3 | 29 |
| D5: Assessment Process (CAP) | 25% | ~43 | 5 | 27 |
| D6: Scoping | 15% | ~26 | 2 | 7 |
| **Total** | | **~170** | **15** | **117** |

**Blueprint coverage: 0/117 skills — run `/cmmc-quiz generate all` to start**

## Coverage Map

```
Sources/Exam-Prep/Generated-Questions/
└── _coverage-map.md    # 117 skills, all GAP — updated by generate/gap-fill
```

## Exam Overview

- **Exam**: CMMC-AB CCP v7.4 Final (10/17/2022)
- **Questions**: 170 multiple choice
- **Length**: 3.5 hours
- **Passing score**: 500 points
- **Prerequisite to**: CCA and CCI certifications

## CCP Domain Reference

### Domain 1 (5%) — CMMC Ecosystem
- Task 1.1: Roles/responsibilities across the ecosystem — OSC, C3PAO, RPO, RP, LPP, LTP, PA, PI, CCP, CCA, CCI, Lead Assessor

### Domain 2 (5%) — Ethics / CoPC
- Task 2.1: CMMC-AB CoPC, ISO/IEC, DoD ethics requirements — 13 items

### Domain 3 (15%) — Governance & Source Documents
- Task 3.1: FCI/CUI regulations — 32 CFR 170, DFARS, CMMC v2.0 levels, non-compliance
- Task 3.2: FCI/CUI roles/authority — FAR 4.1901, EO 13556, DoDI 5200.48
- Task 3.3: CMMC source documents — Model Overview, Assessment Guides, Scoping Guidance, CAP, Glossary, CUI Registry

### Domain 4 (35%) — Model Construct & Implementation Evaluation
- Task 4.1: 14 practice domains (AC, AU, AT, CM, IA, IR, MA, MP, PS, PE, RA, CA, SC, SI) — Level 1 emphasis
- Task 4.2: Assessment methodology — Examine, Interview, Test methods; evidence gathering
- Task 4.3: Evidence adequacy and sufficiency

### Domain 5 (25%) — Assessment Process (CAP)
- Task 5.1: Phase 1 — Plan and Prepare (assessment plan, readiness review)
- Task 5.2: Phase 2 — Conduct Assessment (methods, scoring, team support)
- Task 5.3: Phase 3 — Report Results (preliminary, final, submission)
- Task 5.4: Phase 4 — POA&M Evaluation (minimum score, qualifying items)
- Task 5.5: End-to-end Level 2 Assessment scenario

### Domain 6 (15%) — Scoping
- Task 6.1: High-level scoping — Organization, Host Unit, Supporting Units
- Task 6.2: FCI asset scope — Process/Store/Transmit, out-of-scope, specialized assets, ESP

## Source Documents Available

| Source | Coverage |
|--------|---------|
| `ccp-exam-blueprint-v7-4.md` | Exam guide — 6 domains, 15 tasks, 117 skills |
| `ccp-course-workbook.md` | Full domain curriculum (L1 + L2) |
| `ccp-field-guide-exam-prep.md` | Exam-focused synthesis |
| `ccp-additional-practice-questions.md` | Seeded question bank |
| `workbook-access-control.md` | AC domain deep-dive |
| `workbook-audit-accountability.md` | AU domain deep-dive |
| `workbook-awareness-training.md` | AT domain deep-dive |
| `workbook-configuration-management.md` | CM domain deep-dive |
| `workbook-identification-authentication.md` | IA domain deep-dive |
| `workbook-incident-response.md` | IR domain deep-dive |
| `workbook-maintenance.md` | MA domain deep-dive |
| `workbook-media-protection.md` | MP domain deep-dive |
| `workbook-personnel-security.md` | PS domain deep-dive |
| `workbook-physical-protection.md` | PE domain deep-dive |
| `workbook-risk-assessment.md` | RA domain deep-dive |
| `workbook-security-assessment.md` | CA domain deep-dive |
| `workbook-system-comms-protection.md` | SC domain deep-dive |
| `workbook-system-info-integrity.md` | SI domain deep-dive |
| `cmmc-assessment-process-cap-v5-6-1.md` | Assessment process depth (D5) |
| `cmmc-scoping-guide-level-1-v2.md` | L1 scoping (D6) |
| `cmmc-scoping-guide-level-2-v2.md` | L2 scoping (D6) |
| `32-cfr-part-170-cmmc-program.md` | Regulatory text (D3) |
| `dfars-cmmc-final-rule-federal-register-2025.md` | DFARS rule (D3) |
| `NIST.SP.800-171r2.md` | Authoritative control text (D4) |

## Question Generation Strategy

Domain-specific source mapping:
- **D1 (Ecosystem)**: ccp-course-workbook + ccp-field-guide → ecosystem roles
- **D2 (Ethics)**: ccp-course-workbook → CoPC section
- **D3 (Governance)**: 32-cfr-part-170 + dfars rule + ccp-course-workbook → regulations, source docs, CUI
- **D4 (Model/Practices)**: workbook-*.md files (one per domain) + NIST 800-171 + cmmc-model-overview
- **D5 (Assessment Process)**: cmmc-assessment-process-cap + ccp-field-guide → CAP phases, POA&M
- **D6 (Scoping)**: scoping guides L1/L2 + cap → scoping decisions, specialized assets

## Question Format (same as /quiz-creator)

```markdown
> [!question] Question — Title (Domain N)
> Scenario text...
>
> **A.** Option text
> **B.** Option text
> **C.** Option text
> **D.** Option text

> [!example]- Answer: B
> **A. Incorrect.** Explanation...
> **B. Correct.** Explanation...
> **C. Incorrect.** Explanation...
> **D. Incorrect.** Explanation...
```

Tags:
- `(Domain N)` — required in every title (1-6)
- `(Task X.Y)` — recommended for coverage tracking

## Git Workflow

```bash
# Commit vault changes (questions, sources)
git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault add -A
git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault commit -m "description"

# Commit quiz app changes
cd C:/Users/samue/repos/cmmc-quiz && git add -A && git commit -m "description"
```

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `/quiz-creator` | General-purpose quiz creation (this skill inherits from it) |
| `/cmmc-vault` | Manages the Obsidian vault with sources and wiki articles |
| `/firecrawl` | Scrape CMMC-AB or NIST documentation |
| `/notebooklm` | Analyze sources to find testable concepts per domain |
| `/guided-learning` | Teach weak areas identified by quiz results |
