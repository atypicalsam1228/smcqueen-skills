# Vault Conventions — Obsidian-Native Syntax

This vault uses Obsidian Flavored Markdown. Follow these conventions when creating or editing any file in the Wiki.

## Internal Links

Always use **wikilinks** for internal vault references. Never use standard markdown links for internal files.

```markdown
# Correct
See [[bedrock-model-selection]] for the pattern.
This maps to [[Sources/AWS-Gen-AI/bedrock-developer-guide|Bedrock Developer Guide]].

# Wrong — do not use markdown links for internal vault files
See [bedrock-model-selection](bedrock-model-selection.md).
```

### Link to specific headings

```markdown
[[bedrock-developer-guide#RAG Architecture]]
```

### Display text

```markdown
[[bedrock-developer-guide|Amazon Bedrock Developer Guide]]
```

## Embeds

Use `![[]]` to embed content from source documents inline in Wiki articles. This renders the source text directly inside the article.

```markdown
## Source Reference

![[Sources/AWS-Gen-AI/bedrock-developer-guide#RAG Architecture]]
```

For embedding specific blocks, use block references:

```markdown
![[bedrock-developer-guide#^rag-description]]
```

## Callouts

Use Obsidian callout syntax for structured annotations:

### Source citations (primary use)

```markdown
> [!quote] AWS Bedrock Documentation
> "Amazon Bedrock is a fully managed service that offers a choice of
> high-performing foundation models from leading AI companies."
> — [[Sources/AWS-Gen-AI/bedrock-developer-guide#Overview|Bedrock Overview]]
```

### Knowledge gaps

```markdown
> [!danger] NEEDS SOURCE
> No authoritative source document exists for SageMaker Neo optimization.
> Ingest via `/aws-vault ingest` before citing this topic.
```

### Content drift warnings

```markdown
> [!warning] Citation Drift
> Wiki content in [[bedrock-model-selection]] conflicts with
> [[Sources/AWS-Gen-AI/bedrock-developer-guide]]. Source text updated; wiki needs revision.
```

### Implementation patterns

```markdown
> [!example] AWS Implementation
> Use Amazon Bedrock Knowledge Bases with OpenSearch Serverless
> for a fully managed RAG pipeline with automatic chunking and embedding.
```

### Cross-service relationships

```markdown
> [!info] Cross-Service
> Bedrock Agents integrate with:
> - Lambda for custom actions
> - OpenSearch for vector search
> - S3 for document storage
> - CloudWatch for invocation logging
```

### Exam tips

```markdown
> [!question] AIP-C01 Exam Tip
> Q: Which service provides a fully managed RAG pipeline?
> A: Amazon Bedrock Knowledge Bases — handles chunking, embedding,
> and retrieval automatically.
```

### Foldable callouts

Use `-` for collapsed by default (long reference text), `+` for expanded:

```markdown
> [!quote]- Full Documentation Text (click to expand)
> <lengthy source text here>
```

## Callout Type Reference

| Callout | Use For |
|---|---|
| `> [!quote]` | Verbatim source citations |
| `> [!danger]` | Missing sources, knowledge gaps |
| `> [!warning]` | Citation drift, stale content |
| `> [!example]` | Implementation patterns, code samples |
| `> [!info]` | Cross-service relationships, context |
| `> [!tip]` | Best practices, recommendations |
| `> [!question]` | Exam-style questions and answers |
| `> [!note]` | General notes, clarifications |
| `> [!abstract]` | Executive summaries at top of articles |

## Properties (Frontmatter)

Use Obsidian-typed properties for full graph and search integration:

```yaml
---
type: concept
domain: aws-gen-ai
status: draft
tags:
  - bedrock
  - foundation-models
created: 2026-04-06
updated: 2026-04-06
sources:
  - "[[Sources/AWS-Gen-AI/bedrock-developer-guide]]"
  - "[[Sources/Exam-Prep/ai-professional-01]]"
related:
  - "[[Wiki/rag-patterns-bedrock]]"
  - "[[Wiki/vector-store-comparison]]"
---
```

### Property types

| Property | Obsidian Type | Notes |
|---|---|---|
| `type` | text | concept, pattern, service-overview, architecture, exam-note, guide, session-log |
| `domain` | text | aws-gen-ai, aws-ml, aws-core, aws-security, aws-architecture, exam-prep, cross-service |
| `status` | text | draft, review, final |
| `tags` | list | Freeform, hierarchical allowed (e.g., `bedrock/agents`) |
| `created` | date | YYYY-MM-DD |
| `updated` | date | YYYY-MM-DD |
| `sources` | links | Wikilinks to Sources/ files |
| `related` | links | Wikilinks to other Wiki articles |

The `sources` and `related` properties as **link-type** properties make them visible in Obsidian's graph view — you can see which wiki articles cite which sources.

## Tags

Use hierarchical tags for fine-grained categorization:

```yaml
tags:
  - bedrock/agents
  - bedrock/knowledge-bases
  - sagemaker/training
  - exam-prep/aip-c01
  - architecture/serverless
  - architecture/rag
```

## File Naming

- Kebab-case: `bedrock-model-selection.md`
- Atomic: one concept per note
- Descriptive: filename communicates content without opening
- Wikilink-friendly: avoid special characters that break `[[links]]`
