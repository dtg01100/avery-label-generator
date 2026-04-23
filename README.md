# Avery Label Generator

Generate printable labels from CSV, Excel, or JSON data using Avery sheet formats.

## Install

```bash
pip install -r requirements.txt
```

## Quick Start

### Guided Mode (Interactive)

```bash
python avery_labels.py -i data.xlsx
```

This will prompt you through:
1. Select fields to include on label
2. Choose label format
3. Choose output filename
4. Choose mode (unique or repeat)

### Command Line Mode

```bash
# List available columns in your file
python avery_labels.py -i data.xlsx --list

# List available Avery label formats
python avery_labels.py --list-specs

# Generate labels
python avery_labels.py -i data.xlsx --field "Store Name" --field "Confirmation #" -o labels.pdf
```

## Usage

```
python avery_labels.py [options]

Options:
  -i, --input FILE     Input file (CSV, XLSX, JSON)
  -o, --output FILE   Output PDF file (default: labels.pdf)
  --list             List columns in input file
  --list-specs       List available Avery label formats
  --spec FORMAT      Avery format (e.g., 5960, 5160, 5163)
  -f, --field NAME   Field/column to include on label (can repeat)
  --separator TEXT   Separator between fields (default: newline)
  --mode MODE        unique or repeat (default: unique)
```

## Examples

```bash
# Generate with two fields
python avery_labels.py -i addresses.csv --field Name --field Address --field City -o labels.pdf

# Use specific Avery format
python avery_labels.py -i data.xlsx --spec 5160 --field "Company" -o labels.pdf

# Repeat same label on all slots
python avery_labels.py -i data.csv --mode repeat --field "Return Address" -o labels.pdf

# Custom separator (comma between fields)
python avery_labels.py -i data.csv --field Name --field Phone --separator ", " -o labels.pdf
```

## Label Formats

| Format | Layout | Labels/Sheet |
|--------|--------|--------------|
| 5960 | 3×10 | 30 |
| 5160 | 3×10 | 30 |
| 5163 | 2×5 | 10 |
| 5164 | 2×3 | 6 |

Run `python avery_labels.py --list-specs` to see all 80+ available formats.

## Input Data

Supported formats:
- **CSV** - First row should be headers
- **Excel** (.xlsx, .xls) - First row = headers
- **JSON** - Array of objects

Empty rows are automatically skipped.

## Output

Generates a PDF ready to print on your label sheets. Make sure to:
- Print at **100% scale** (not "fit to page")
- Use **Letter** paper size
- Load labels correctly in your printer (usually top feed)