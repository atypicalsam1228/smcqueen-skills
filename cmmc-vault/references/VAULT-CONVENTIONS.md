# Vault Conventions — Obsidian-Native Syntax

This vault uses Obsidian Flavored Markdown. Follow these conventions when creating or editing any file in the Wiki.

## Internal Links

Always use **wikilinks** for internal vault references. Never use standard markdown links for internal files.

```markdown
# Correct
See [[ac-access-control-overview]] for the practice breakdown.
This maps to [[Sources/NIST-800-171/sp800-171r2|NIST SP 800-171 Rev 2]].

# Wrong — do not use markdown links for internal vault files
See [ac-access-control-overview](ac-access-control-overview.md).
```

### Link to specific headings

```markdown
[[sp800-171r2#3.1 Access Control]]
```

### Display text

```markdown
[[sp800-171r2|NIST SP 800-171 Rev 2]]
```

## Embeds

Use `![[]]` to embed content from source documents inline in Wiki articles. This renders the source text directly inside the article.

```markdown
## Source Reference

![[Sources/NIST-800-171/sp800-171r2#3.1 Access Control]]
```

For embedding specific blocks, use block references:

```markdown
![[sp800-171r2#^ac-1-1]]
```

## Callouts

Use Obsidian callout syntax for structured annotations:

### Source citations (primary use)

```markdown
> [!quote] NIST SP 800-171 Rev 2
> "Limit system access to authorized users, processes acting on behalf of authorized users,
> and devices (including other systems)."
> — [[Sources/NIST-800-171/sp800-171r2#3.1.1|3.1.1 Access Control]]
```

### Knowledge gaps

```markdown
> [!danger] NEEDS SOURCE
> No authoritative source document exists for CMMC Level 3 delta requirements.
> Ingest via `/cmmc-vault ingest` before citing this topic.
```

### Content drift warnings

```markdown
> [!warning] Citation Drift
> Wiki content in [[ac-access-control-overview]] conflicts with
> [[Sources/CMMC-Model/cmmc-model-v2-0]]. Source text updated; wiki needs revision.
```

### Implementation patterns

```markdown
> [!example] Implementation Guidance
> Implement MFA for all privileged accounts using PIV/CAC or a TOTP software token.
> Document in SSP Section 3.5 under IA.2.078.
```

### Cross-domain relationships

```markdown
> [!info] Cross-Domain
> AC.1.001 (access control) interacts with:
> - IA.1.076 / IA.1.077 (identification and authentication)
> - AU.2.041 (audit logging of access events)
> - CM.2.061 (authorized software/system configurations)
```

### Exam tips

```markdown
> [!question] CCP Exam Tip
> Q: What is the minimum number of CMMC Level 2 practices?
> A: 110 practices, all drawn from NIST SP 800-171 Rev 2.
```

### Foldable callouts

Use `-` for collapsed by default (long reference text), `+` for expanded:

```markdown
> [!quote]- Full Control Text (click to expand)
> <lengthy source text here>
```

## Callout Type Reference

| Callout | Use For |
|---|---|
| `> [!quote]` | Verbatim source citations |
| `> [!danger]` | Missing sources, knowledge gaps |
| `> [!warning]` | Citation drift, stale content |
| `> [!example]` | Implementation patterns, SSP language |
| `> [!info]` | Cross-domain relationships, context |
| `> [!tip]` | Best practices, assessment tips |
| `> [!question]` | Exam-style questions and answers |
| `> [!note]` | General notes, clarifications |
| `> [!abstract]` | Executive summaries at top of articles |

## Properties (Frontmatter)

Use Obsidian-typed properties for full graph and search integration:

```yaml
---
type: concept
domain: access-control
cmmc-level: level-2
status: draft
tags:
  - access-control
  - AC.1.001
  - nist-800-171
created: 2026-04-27
updated: 2026-04-27
sources:
  - "[[Sources/NIST-800-171/sp800-171r2]]"
  - "[[Sources/CMMC-Model/cmmc-model-v2-0]]"
related:
  - "[[Wiki/ia-identification-authentication]]"
  - "[[Wiki/au-audit-accountability-overview]]"
---
```

### Property types

| Property | Obsidian Type | Notes |
|---|---|---|
| `type` | text | concept, pattern, practice-overview, architecture, exam-note, guide, ssp-template, session-log |
| `domain` | text | access-control, asset-management, audit-accountability, configuration-management, identification-auth, incident-response, maintenance, media-protection, personnel-security, physical-protection, recovery, risk-management, security-assessment, situational-awareness, system-comms-protection, system-info-integrity, cui-handling, assessment-prep, cross-domain |
| `cmmc-level` | text | level-1, level-2, level-3, all-levels |
| `status` | text | draft, review, final |
| `tags` | list | Freeform, hierarchical (e.g., `access-control/AC.1.001`) |
| `created` | date | YYYY-MM-DD |
| `updated` | date | YYYY-MM-DD |
| `sources` | links | Wikilinks to Sources/ files — visible in graph view |
| `related` | links | Wikilinks to other Wiki articles — visible in graph view |

The `sources` and `related` properties as **link-type** properties make them visible in Obsidian's graph view.

## Tags

Use hierarchical tags for fine-grained categorization:

```yaml
tags:
  - access-control/AC.1.001
  - access-control/least-privilege
  - nist-800-171/3.1
  - cmmc-level-2
  - exam-prep/ccp
  - cui-handling
  - ssp-template
```

## File Naming

- Kebab-case: `ac-access-control-overview.md`
- Prefix practice-specific notes with domain abbreviation: `ac-`, `ia-`, `cm-`, `au-`, etc.
- Atomic: one concept per note
- Descriptive: filename communicates content without opening
- Wikilink-friendly: avoid special characters that break `[[links]]`
- Prefer flat/shallow over deep nesting
