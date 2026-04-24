# Avery Labels - uv tool install Design

## Context

User wants `uv tool install .` to work and automatically launch the web UI.

## Design

### Approach

Add `pyproject.toml` with `[project.scripts]` entry point. Refactor `app.py` to expose a `main()` function that `uv` can call.

### Files

**Modify: `pyproject.toml` (new)**
```toml
[project]
name = "avery-labels"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = ["flask", "openpyxl", "reportlab"]

[project.scripts]
avery-labels = "app:main"
```

**Modify: `app.py`**
Wrap `app.run()` in `main()` function:
```python
def main():
    app.run(debug=True, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    main()
```

**Modify: `requirements.txt`**
Remove flask (now in pyproject.toml), keep other deps.

### Usage

```bash
uv tool install .
avery-labels  # opens web UI at http://localhost:5000
```

### No Changes
- Keep existing CLI in `avery_labels.py` (separate entry point)
- `app.py` serves both direct run (`python app.py`) and tool install (`avery-labels`)
