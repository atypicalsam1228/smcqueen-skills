---
name: docx-to-markdown
description: Convert a Word document (.docx) to Markdown (.md) with copyable code blocks, converting Linux commands to PowerShell and non-Python code to Python.
user-invocable: true
---

# Word Document to Markdown with Code Blocks

Convert a Word document (.docx) to a Markdown (.md) file, wrapping all commands and code snippets in fenced code blocks so readers can use the copy button.

## Trigger

Use this skill when:
- The user asks to convert a Word document to Markdown
- The user wants to make commands in a document copyable
- The user asks to create a .md version of a .docx file

## Instructions

1. **Read the Word document** using `python-docx` to extract all text content, preserving headings, paragraphs, lists, and tables.

2. **Identify all commands and code snippets** in the document. These include:
   - Shell/terminal commands (lines starting with `$`, `#`, `python`, `pip`, `aws`, `curl`, `git`, `docker`, `npm`, `cd`, `mkdir`, `ls`, `chmod`, `cat`, `source`, etc.)
   - Python code (imports, function definitions, variable assignments, print statements, etc.)
   - Configuration files (YAML, JSON, Dockerfiles, etc.)
   - Any text formatted as code in the original document (monospace font)
   - Multi-line code blocks that appear as contiguous command/code lines

3. **Wrap each command or code block** in a fenced code block with the appropriate language tag:
   ````
   ```bash
   pip install scikit-learn pandas numpy flask joblib
   ```
   ````

   ````
   ```python
   import pandas as pd
   model = RandomForestClassifier(n_estimators=100)
   ```
   ````

   ````
   ```powershell
   Get-FileHash fraud_model.pkl -Algorithm SHA256
   ```
   ````

4. **Preserve document structure**:
   - Convert Word headings to Markdown headings (`#`, `##`, `###`)
   - Convert bullet lists to Markdown lists (`-` or `*`)
   - Convert numbered lists to Markdown numbered lists (`1.`, `2.`, etc.)
   - Convert tables to Markdown tables
   - Preserve bold (`**text**`) and italic (`*text*`) formatting
   - Keep "Expected Output" sections as code blocks with no language tag

5. **Identify "Expected Output" blocks** — text that shows what the terminal will display after running a command. Wrap these in plain code blocks (no language tag):
   ````
   ```
   Dataset saved: 10000 rows, 500 fraud cases
   ```
   ````

6. **Convert all Linux/Mac shell commands to PowerShell equivalents**:
   - `cat > file.py << 'EOF' ... EOF` → `@" ... "@ | Out-File -Encoding utf8 file.py`
   - `source venv/bin/activate` → `.\venv\Scripts\Activate`
   - `mkdir -p ~/dir` → `New-Item -ItemType Directory -Force -Path ~/dir`
   - `chmod 444 file` → `Set-ItemProperty file -Name IsReadOnly -Value $true`
   - `ls -lh file` → `dir file` or `Get-ChildItem file`
   - `sha256sum file` → `Get-FileHash file -Algorithm SHA256`
   - `curl -s url` → `Invoke-RestMethod url`
   - `python3` → `python`
   - `pip install` → `python -m pip install`
   - `pip freeze` → `python -m pip freeze`
   - `pkill -f process` → `Stop-Process -Name process`
   - `cat file` → `Get-Content file`
   - `export VAR=value` → `$env:VAR = "value"`
   - Forward slashes in paths → backslashes where appropriate
   - Tag all converted commands as `powershell` in code blocks

7. **Convert non-Python code to Python** where applicable:
   - If the document contains code snippets in other languages (JavaScript, Ruby, Go, etc.) that are used for demonstration, convert them to Python equivalents
   - Preserve the same logic and functionality
   - Use idiomatic Python (PEP 8 style, standard library where possible)
   - Tag converted code as `python` in code blocks
   - Add a note indicating the original language if the conversion changes behavior

8. **Save the output** as a `.md` file in the same directory as the source document, using the same base filename.

## Language Tag Reference

| Content Type | Language Tag |
|---|---|
| Linux/Mac shell commands | `bash` |
| PowerShell commands | `powershell` |
| Python code | `python` |
| JSON | `json` |
| YAML | `yaml` |
| Dockerfile | `dockerfile` |
| SQL | `sql` |
| Plain output / expected results | (no tag) |
