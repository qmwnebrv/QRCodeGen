import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.labels import DEFAULT_PRESET, LABEL_PRESETS
from app.pdf_gen import generate_pdf
from app.preview import PreviewWindow
from app.qr_utils import make_qr_bytes


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("QR Label Generator")
        self.root.resizable(False, False)

        self._rows: list[dict] = []
        self._ids: list[str] = []
        self._qr_cache: dict[str, bytes] = {}

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        f = tk.Frame(self.root, padx=18, pady=14)
        f.pack()

        # Row 0 – CSV loader
        tk.Button(f, text="Load CSV", width=14, command=self._load_csv).grid(
            row=0, column=0, pady=4, sticky="w"
        )
        self._file_lbl = tk.Label(f, text="No file loaded", fg="grey", anchor="w")
        self._file_lbl.grid(row=0, column=1, padx=10, sticky="w")

        # Row 1 – column selector
        tk.Label(f, text="ID Column:").grid(row=1, column=0, sticky="w", pady=(6, 2))
        self._col_var = tk.StringVar()
        self._col_cb = ttk.Combobox(f, textvariable=self._col_var, state="disabled", width=26)
        self._col_cb.grid(row=1, column=1, padx=10, sticky="w", pady=(6, 2))
        self._col_cb.bind("<<ComboboxSelected>>", self._on_col)

        # Row 2 – label type selector
        tk.Label(f, text="Label Type:").grid(row=2, column=0, sticky="w", pady=(4, 2))
        preset_names = [p["name"] for p in LABEL_PRESETS.values()]
        self._preset_name_var = tk.StringVar(value=LABEL_PRESETS[DEFAULT_PRESET]["name"])
        self._preset_cb = ttk.Combobox(
            f,
            textvariable=self._preset_name_var,
            values=preset_names,
            state="readonly",
            width=38,
        )
        self._preset_cb.grid(row=2, column=1, padx=10, sticky="w", pady=(4, 2))

        # Row 3 – status line
        self._status_lbl = tk.Label(f, text="", fg="grey")
        self._status_lbl.grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))

        # Row 4 – action buttons
        btn_f = tk.Frame(f)
        btn_f.grid(row=4, column=0, columnspan=2, pady=10)

        self._prev_btn = tk.Button(
            btn_f, text="Preview", width=12, state="disabled", command=self._preview
        )
        self._prev_btn.pack(side="left", padx=4)

        self._exp_btn = tk.Button(
            btn_f, text="Export PDF", width=12, state="disabled", command=self._export
        )
        self._exp_btn.pack(side="left", padx=4)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _selected_preset_key(self) -> str:
        selected_name = self._preset_name_var.get()
        for key, preset in LABEL_PRESETS.items():
            if preset["name"] == selected_name:
                return key
        return DEFAULT_PRESET

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _load_csv(self) -> None:
        path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh)
                self._rows = list(reader)
                cols = list(reader.fieldnames or [])
        except Exception as exc:
            messagebox.showerror("Load error", f"Could not read CSV:\n{exc}")
            return

        if not cols:
            messagebox.showwarning("Empty file", "No columns detected in the CSV.")
            return

        self._file_lbl.config(text=path.split("/")[-1], fg="black")
        self._col_cb.config(values=cols, state="readonly")
        self._col_var.set(cols[0])
        self._extract_ids(warn_empty=False)

    def _on_col(self, _event=None) -> None:
        self._extract_ids(warn_empty=True)

    def _extract_ids(self, warn_empty: bool) -> None:
        col = self._col_var.get()
        seen: set[str] = set()
        ids: list[str] = []
        empty = 0

        for row in self._rows:
            val = (row.get(col) or "").strip()
            if not val:
                empty += 1
                continue
            if val in seen:
                continue
            seen.add(val)
            ids.append(val)

        self._ids = ids
        self._qr_cache = {}

        enabled = "normal" if ids else "disabled"
        self._prev_btn.config(state=enabled)
        self._exp_btn.config(state=enabled)

        status = f"{len(ids)} unique ID(s)"
        if empty:
            status += f"   |   {empty} empty row(s) skipped"
            if warn_empty:
                messagebox.showwarning(
                    "Empty IDs skipped",
                    f"{empty} row(s) had no value in '{col}' and were skipped.",
                )
        self._status_lbl.config(text=status)

    def _build_cache(self) -> None:
        for label_id in self._ids:
            if label_id not in self._qr_cache:
                self._qr_cache[label_id] = make_qr_bytes(label_id)

    def _preview(self) -> None:
        self._build_cache()
        PreviewWindow(self.root, self._ids, self._qr_cache, self._selected_preset_key())

    def _export(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not path:
            return

        self._build_cache()
        try:
            generate_pdf(self._ids, self._qr_cache, path, self._selected_preset_key())
            messagebox.showinfo("Exported", f"PDF saved:\n{path}")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))
