# Avery Label Generator - Web UI Design

## Context

The avery-label-generator project generates printable PDF labels from CSV/Excel/JSON data using Avery sheet specifications. The core logic works well (as CLI), but the interactive CLI prompts are clunky. A simple web UI would make the tool more accessible.

## Design

### Stack
- **Flask** (Python web framework) - thin wrapper around existing `avery_labels.py` functions
- **HTML templates** - Jinja2 templates, minimal CSS
- **No JavaScript frameworks** - vanilla JS only if needed for file handling
- Keep existing `avery_labels.py` unchanged

### Endpoints

**`GET /`** - Main form
- File upload (CSV/XLSX/JSON)
- Field selection (multi-select checkboxes, populated after upload)
- Label format dropdown (populated from `avery_specs.csv`)
- Mode toggle (unique/repeat)
- Output filename input
- Generate button

**`POST /upload`** - Handle file upload
- Accept uploaded file, parse columns
- Return list of column names as JSON for field checkboxes

**`POST /generate`** - Generate PDF
- Receive: filename, selected fields, spec name, mode
- Call existing `avery_labels.py` functions via import
- Return PDF as download response

### Architecture

```
app.py              Flask routes (upload, generate)
templates/
  index.html        Main form page
static/
  style.css         Minimal styling
avery_labels.py     Core logic (unchanged)
```

### Constraints
- Local-only, single-user
- No authentication/sessions needed
- File uploads saved temporarily, cleaned up after generation
- No preview/stretch goal for now - just form → PDF download

### Security Notes
- Validate uploaded file type by extension and content
- Limit file upload size (e.g., 10MB max)
- Clean up temp files after download

## File: app.py

```python
from flask import Flask, render_template, request, send_file, jsonify
from avery_labels import read_input, generate_labels, load_specs_from_csv, format_label_text
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def index():
    specs = load_specs_from_csv()
    return render_template("index.html", specs=sorted(specs.keys()), spec_default="5960")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    # ... parse columns, return JSON

@app.route("/generate", methods=["POST"])
def generate():
    # ... call avery_labels, return PDF
```

## File: templates/index.html

Single page with:
- File upload form
- Dynamic field checkboxes (populated via /upload)
- Spec dropdown (pre-populated from Flask)
- Mode radio buttons
- Submit triggers /generate

## Out of Scope
- Label preview (stretch goal)
- Multi-user / auth
- Deployable hosting