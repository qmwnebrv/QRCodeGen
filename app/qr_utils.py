import io

import qrcode
from qrcode.constants import ERROR_CORRECT_L


def make_qr_bytes(data: str) -> bytes:
    """Return PNG bytes for a QR code encoding *data*."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    buf = io.BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    return buf.getvalue()
