import io

import barcode
from barcode.writer import ImageWriter


def make_barcode_bytes(data: str) -> bytes:
    """Return PNG bytes for a Code 128 barcode encoding *data*.

    Code 128 supports the full ASCII character set (0–127).
    """
    writer = ImageWriter()
    code = barcode.get("code128", data, writer=writer)
    buf = io.BytesIO()
    code.write(buf, options={"write_text": False, "quiet_zone": 1})
    return buf.getvalue()
