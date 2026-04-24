# uv tool install Implementation Plan

> **For agentic workers:** Execute task-by-task.

**Goal:** Enable `uv tool install .` and run `avery-labels` to open web UI.

**Architecture:** Add pyproject.toml with console script entry point. Refactor app.py for main() function.

---

### Task 1: Create pyproject.toml and refactor app.py

**Files:**
- Create: `pyproject.toml`
- Modify: `app.py`
- Modify: `requirements.txt`

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "avery-labels"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = [
    "flask>=3.0.0",
    "openpyxl>=3.0.0",
    "reportlab>=4.0.0",
]

[project.scripts]
avery-labels = "app:main"
```

- [ ] **Step 2: Modify app.py - add main() function**

```python
def main():
    app.run(debug=True, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Update requirements.txt - remove flask**

Keep only non-flask dependencies:
```
openpyxl
reportlab
```

- [ ] **Step 4: Test**

```bash
uv tool install .
avery-labels &
# Visit http://localhost:5000
```

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml app.py requirements.txt
git commit -m "feat: add pyproject.toml for uv tool install"
```
