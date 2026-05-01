# 1 mm expressed in ReportLab points  (72 pt/inch ÷ 25.4 mm/inch)
MM = 72 / 25.4

# ---------------------------------------------------------------------------
# Label preset catalogue
# ---------------------------------------------------------------------------
# Each entry fully describes the physical layout of one Avery label sheet.
# All dimensions are in ReportLab points so pdf_gen can use them directly.
#
# To add a new preset, copy an existing entry and change the values.
# Keys are the product codes shown in the UI dropdown.
# ---------------------------------------------------------------------------
LABEL_PRESETS: dict = {
    "L7159": {
        "name": "Avery L7159 – 64×33.8 mm (24/sheet)",
        # Grid
        "cols": 3,
        "rows": 8,
        # Label face size
        "label_w": 64.0 * MM,      # pt
        "label_h": 33.8 * MM,      # pt
        # Sheet margins (edge of paper → edge of first label)
        "margin_top":  13.3 * MM,  # pt
        "margin_left":  7.2 * MM,  # pt
        # Gaps between adjacent labels
        "col_gap":  1.8 * MM,      # pt  (horizontal)
        "row_gap":  0.0 * MM,      # pt  (vertical – labels are flush)
        # Math check (A4 = 210 × 297 mm):
        #   3×64 + 2×1.8 + 2×7.2  = 192+3.6+14.4 = 210 ✓
        #   8×33.8 + 7×0  + 2×13.3 = 270.4+0+26.6 = 297 ✓
    },
    "AV980016": {
        "name": "Avery 980016 – 45×45 mm (20/sheet)",
        # Grid
        "cols": 4,
        "rows": 5,
        # Label face size
        "label_w": 45 * MM,       # pt
        "label_h": 45 * MM,       # pt
        # Sheet margins (edge of paper → edge of first label)
        "margin_top":  13.5 * MM,  # pt
        "margin_left":  7.5 * MM,  # pt
        # Gaps between adjacent labels
        "col_gap":  5.00 * MM,     # pt  (horizontal)
        "row_gap": 11.25 * MM,     # pt  (vertical)
        # Math check (A4 = 210 × 297 mm):
        #   4×45 + 3×5   + 2×7.5  = 180+15+15  = 210 ✓
        #   5×45 + 4×11.25 + 2×13.5 = 225+45+27 = 297 ✓
    },
}

DEFAULT_PRESET = "AV980016"
