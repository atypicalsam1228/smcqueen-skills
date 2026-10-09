# cmmc-vault skill

Manages the CMMC knowledge Obsidian vault at `C:/Users/samue/OneDrive/Obsidian/CMMC_Vault`.

## Invoke

```
/cmmc-vault <subcommand>
```

## Subcommands

| Subcommand | Description |
|---|---|
| `status` | Vault stats, file counts, git status |
| `compile` | Process Capture/ inbox into Wiki articles |
| `query <question>` | Search vault with source verification |
| `ingest <path>` | Add document to Sources/ |
| `extract [path\|all]` | Extract text from PDFs in Sources/ |
| `lint` | Vault health checks |
| `index` | Regenerate all indexes |

## References

- `references/CMMC-PRACTICE-IDENTIFIERS.md` — Practice domain/ID lookup table
- `references/VAULT-CONVENTIONS.md` — Obsidian syntax rules

## Vault

- Path: `C:/Users/samue/OneDrive/Obsidian/CMMC_Vault`
- Git: `C:/Users/samue/repos/cmmc_vault.git` (bare repo, separate from OneDrive)
