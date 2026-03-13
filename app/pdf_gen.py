import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as rl_canvas

from app.labels import DEFAULT_PRESET, LABEL_PRESETS

PAGE_W, PAGE_H = A4

# ---------------------------------------------------------------------------
# Internal label layout constants (padding / text area inside each label cell)
# ---------------------------------------------------------------------------
PAD    = 4.0   # pt – gap between label edge and content
TEXT_H = 14.0  # pt – height reserved for the ID text line
GAP    = 3.0   # pt – space between the QR image and the text


def _qr_size(label_h: float) -> float:
    """QR image side length (square) that fits inside a label of given height."""
    return label_h - 2 * PAD - TEXT_H - GAP


def _fit_font(c: rl_canvas.Canvas, text: str, max_w: float, start: int = 11) -> int:
    size = start
    while size > 4 and c.stringWidth(text, "Helvetica", size) > max_w:
        size -= 1
    return size


def draw_label(
    c: rl_canvas.Canvas,
    x: float,
    y: float,
    label_id: str,
    qr_bytes: bytes,
    label_w: float,
    label_h: float,
) -> None:
    """Draw one label. x, y = bottom-left corner in PDF points."""
    qr_size = _qr_size(label_h)
    qr_x = x + (label_w - qr_size) / 2
    qr_y = y + TEXT_H + GAP
    c.drawImage(ImageReader(io.BytesIO(qr_bytes)), qr_x, qr_y, qr_size, qr_size)

    fs = _fit_font(c, label_id, label_w - 2 * PAD)
    c.setFont("Helvetica", fs)
    tw = c.stringWidth(label_id, "Helvetica", fs)
    c.drawString(x + (label_w - tw) / 2, y + PAD, label_id)


def generate_pdf(
    ids: list,
    qr_cache: dict,
    output_path: str,
    preset_key: str = DEFAULT_PRESET,
) -> None:
    p          = LABEL_PRESETS[preset_key]
    cols       = p["cols"]
    rows       = p["rows"]
    label_w    = p["label_w"]
    label_h    = p["label_h"]
    margin_top  = p["margin_top"]
    margin_left = p["margin_left"]
    col_gap    = p["col_gap"]
    row_gap    = p["row_gap"]
    per_page   = cols * rows

    c = rl_canvas.Canvas(output_path, pagesize=A4)

    for i, label_id in enumerate(ids):
        if i > 0 and i % per_page == 0:
            c.showPage()

        idx = i % per_page
        col, row = idx % cols, idx // cols
        x = margin_left + col * (label_w + col_gap)
        y = PAGE_H - margin_top - row * (label_h + row_gap) - label_h

        draw_label(c, x, y, label_id, qr_cache[label_id], label_w, label_h)

    c.save()
