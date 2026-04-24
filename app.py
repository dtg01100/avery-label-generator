#!/usr/bin/env python3
"""Flask web UI for Avery Label Generator."""

import os
import sys
import tempfile
import webbrowser
from io import BytesIO

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, send_file, jsonify
from avery_labels import read_input, generate_labels, load_specs_from_csv, format_label_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB max

SPECS_FILE = "avery_specs.csv"

@app.route("/")
def index():
    specs = load_specs_from_csv()
    return render_template("index.html", specs=sorted(specs.keys()), spec_default="5960")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".csv", ".xlsx", ".xls", ".json"]:
        return jsonify({"error": "Unsupported file type"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        try:
            data = read_input(tmp.name)
            columns = list(data[0].keys()) if data else []
        finally:
            os.unlink(tmp.name)

    return jsonify({"columns": columns})

@app.route("/generate", methods=["POST"])
def generate():
    file = request.files.get("file")
    fields = request.form.getlist("fields")
    spec_name = request.form.get("spec")
    mode = request.form.get("mode", "unique")
    output_name = request.form.get("output", "labels.pdf")

    if not file or not fields or not spec_name:
        return jsonify({"error": "Missing required fields"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        try:
            data = read_input(tmp.name)
            specs = load_specs_from_csv()
            if spec_name not in specs:
                return jsonify({"error": f"Unknown spec: {spec_name}"}), 400

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as out:
                try:
                    generate_labels(
                        data=data,
                        output=out.name,
                        specs=specs[spec_name],
                        fields=fields,
                        mode=mode,
                    )
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
                with open(out.name, 'rb') as f:
                    content = f.read()
                os.unlink(out.name)
            return send_file(
                BytesIO(content),
                download_name=output_name,
                as_attachment=True,
                mimetype='application/pdf'
            )
        finally:
            os.unlink(tmp.name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--nolaunch", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()

    host = "127.0.0.1"
    port = 5000

    if not args.nolaunch:
        url = f"http://{host}:{port}"
        print(f"Opening {url}")
        webbrowser.open(url)

    app.run(debug=False, host=host, port=port)
