# Vault Conventions — Obsidian-Native Syntax

This vault uses Obsidian Flavored Markdown. Follow these conventions when creating or editing any file in the Wiki.

## Internal Links

Always use **wikilinks** for internal vault references. Never use standard markdown links for internal files.

```markdown
# Correct
See [[least-privilege-implementation]] for the pattern.
This maps to [[Sources/NIST-800-53/AC-access-control|AC Access Control]].

# Wrong — do not use markdown links for internal vault files
See [least-privilege-implementation](least-privilege-implementation.md).
```

### Link to specific headings

```markdown
[[AC-access-control#AC-2 Account Management]]
```

### Display text

```markdown
[[AC-access-control|AC Access Control]]
```

## Embeds

Use `![[]]` to embed content from source documents inline in Wiki articles. This renders the source text directly inside the article.

```markdown
## Source Reference

![[Sources/NIST-800-53/AC-access-control#AC-2 Account Management]]
```

For embedding specific blocks, use block references:

```markdown
![[AC-access-control#^ac2-description]]
```

## Callouts

Use Obsidian callout syntax for compliance-specific signals:

### Source citations (primary use)

```markdown
> [!quote] NIST 800-53 AC-2
> The organization manages information system accounts, including establishing,
> activating, modifying, reviewing, disabling, and removing accounts.
> — [[Sources/NIST-800-53/AC-access-control#AC-2 Account Management]]
```

### Compliance warnings

```markdown
> [!warning] Citation Drift
> Wiki content in [[least-privilege-implementation]] conflicts with
> [[Sources/NIST-800-53/AC-6]]. Source text updated; wiki needs revision.
```

### Missing sources

```markdown
> [!danger] NEEDS SOURCE
> No authoritative source document exists for OWASP LLM03.
> Ingest via `/rmf-vault ingest` before citing this control.
```

### Implementation patterns

```markdown
> [!example] AWS Implementation
> Enforce least privilege using IAM permission boundaries with
> `iam:PermissionsBoundary` condition keys.
```

### Cross-framework notes

```markdown
> [!info] Cross-Framework Mapping
> This control maps to:
> - FedRAMP Moderate: Required (AC-6)
> - NIST 800-171: 3.1.5 (Least Privilege)
> - OWASP LLM: LLM06 (Excessive Agency)
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
| `> [!warning]` | Citation drift, stale content |
| `> [!danger]` | Missing sources, compliance gaps |
| `> [!example]` | Implementation patterns, AWS examples |
| `> [!info]` | Cross-framework mappings, context |
| `> [!tip]` | Best practices, recommendations |
| `> [!note]` | General notes, clarifications |
| `> [!abstract]` | Executive summaries at top of articles |

## Properties (Frontmatter)

Use Obsidian-typed properties for full graph and search integration:

```yaml
---
type: concept
framework: nist-800-53
status: draft
tags:
  - access-control
  - least-privilege
created: 2026-04-05
updated: 2026-04-05
sources:
  - "[[Sources/NIST-800-53/AC-access-control]]"
  - "[[Sources/FedRAMP/fedramp-moderate-baseline]]"
related:
  - "[[Wiki/fedramp-moderate-access-controls]]"
  - "[[Wiki/least-privilege-across-frameworks]]"
---
```

### Property types

| Property | Obsidian Type | Notes |
|---|---|---|
| `type` | text | concept, pattern, decision-record, mapping, guide, session-log |
| `framework` | text | nist-800-53, fedramp, nist-ai-rmf, owasp-llm, nist-800-171, cross-framework |
| `status` | text | draft, review, final |
| `tags` | list | Freeform, hierarchical allowed (e.g., `access-control/least-privilege`) |
| `created` | date | YYYY-MM-DD |
| `updated` | date | YYYY-MM-DD |
| `sources` | links | Wikilinks to Sources/ files |
| `related` | links | Wikilinks to other Wiki articles |

The `sources` and `related` properties as **link-type** properties make them visible in Obsidian's graph view — you can see which wiki articles cite which sources.

## Tags

Use hierarchical tags for fine-grained categorization:

```yaml
tags:
  - access-control/account-management
  - fedramp/moderate
  - implementation/aws
```

## File Naming

- Kebab-case: `least-privilege-implementation.md`
- Atomic: one concept per note
- Descriptive: filename communicates content without opening
- Wikilink-friendly: avoid special characters that break `[[links]]`
