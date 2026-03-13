# QR Label Generator

Desktop app that loads a CSV, lets you pick a sample ID column, choose an Avery label format, and exports a multi-page A4 PDF of QR code labels — sized to match the physical sheet exactly.

---

## Setup

### Option A — conda (recommended)

```bash
conda env create -f environment.yml
conda activate qrcode-machine
```

### Option B — pip + venv

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Workflow

1. Click **Load CSV** and select your file.
2. Choose the column that contains your sample IDs.
3. Choose your **Label Type** (Avery product code) from the dropdown.
4. Click **Preview** to see page 1 of the generated labels.
5. Click **Export PDF** and choose a save location. All pages are exported.

---

## Label formats

| Product code | Name | Size | Grid | Per sheet |
|---|---|---|---|---|
| AV980016 | Avery 980016 | 45 × 45 mm | 4 × 5 | 20 |

Adding a new format is one dict entry in `app/labels.py`.

---

## Label layout

| Property | Value |
|---|---|
| Page size | A4 |
| QR error correction | Level L |
| Content | QR code + human-readable ID below |
| Long IDs | Font auto-scales to fit within the label |
| Duplicates | Skipped automatically |
| Empty cells | Warned and skipped |

---

## Project structure

```
QRCODE_Machine/
├── main.py            # Entry point
├── requirements.txt
├── environment.yml
├── README.md
└── app/
    ├── gui.py         # Tkinter main window
    ├── labels.py      # Avery label preset catalogue
    ├── pdf_gen.py     # ReportLab PDF generation
    ├── preview.py     # Tkinter preview window (page 1)
    └── qr_utils.py    # QR code byte generation
```
