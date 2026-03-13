import io
import tkinter as tk

from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4

from app.labels import DEFAULT_PRESET, LABEL_PRESETS
from app.pdf_gen import GAP, PAD, _qr_size

PAGE_W, PAGE_H = A4
PREVIEW_W = 530
SCALE     = PREVIEW_W / PAGE_W
PREVIEW_H = int(PAGE_H * SCALE)


class PreviewWindow(tk.Toplevel):
    """Shows a scaled preview of the first page."""

    def __init__(
        self,
        parent: tk.Tk,
        ids: list,
        qr_cache: dict,
        preset_key: str = DEFAULT_PRESET,
    ) -> None:
        super().__init__(parent)
        self.resizable(False, False)
        self._refs: list = []

        p           = LABEL_PRESETS[preset_key]
        cols        = p["cols"]
        rows        = p["rows"]
        label_w     = p["label_w"]
        label_h     = p["label_h"]
        margin_top  = p["margin_top"]
        margin_left = p["margin_left"]
        col_gap     = p["col_gap"]
        row_gap     = p["row_gap"]
        per_page    = cols * rows
        qr_size     = _qr_size(label_h)

        shown = min(len(ids), per_page)
        self.title(f"Preview – Page 1  ({shown} of {len(ids)} labels)")

        canvas = tk.Canvas(self, width=PREVIEW_W, height=PREVIEW_H, bg="white")
        canvas.pack()

        for i, label_id in enumerate(ids[:per_page]):
            col, row = i % cols, i // cols

            # Label top-left in screen pixels
            lx = (margin_left + col * (label_w + col_gap)) * SCALE
            ly = (margin_top  + row * (label_h + row_gap)) * SCALE
            lw = label_w * SCALE

            # QR image
            qr_s = int(qr_size * SCALE)
            qr_x = lx + (lw - qr_s) / 2
            qr_y = ly + PAD * SCALE

            img = Image.open(io.BytesIO(qr_cache[label_id])).resize(
                (qr_s, qr_s), Image.LANCZOS
            )
            photo = ImageTk.PhotoImage(img)
            self._refs.append(photo)
            canvas.create_image(qr_x, qr_y, anchor="nw", image=photo)

            # ID text – shrink font until it fits within the label width
            text_y     = qr_y + qr_s + GAP * SCALE
            max_text_w = (label_w - 2 * PAD) * SCALE
            fs = max(5, int(9 * SCALE))
            _tmp = canvas.create_text(0, -9999, text=label_id, font=("Helvetica", fs))
            while fs > 5:
                canvas.itemconfig(_tmp, font=("Helvetica", fs))
                bbox = canvas.bbox(_tmp)
                if bbox and (bbox[2] - bbox[0]) <= max_text_w:
                    break
                fs -= 1
            canvas.delete(_tmp)
            canvas.create_text(
                lx + lw / 2,
                text_y,
                text=label_id,
                font=("Helvetica", fs),
                anchor="n",
            )
