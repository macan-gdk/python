"""UI local Tkinter — chọn file và xuất txt/docx (Linux / Windows / macOS).

Cài Tk:
  Ubuntu/Debian:  sudo apt install python3-tk
  Fedora:         sudo dnf install python3-tkinter
  Windows/macOS:  Python từ python.org (tick tcl/tk)
"""

from __future__ import annotations

import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from doc_tool import export_attachment

APP_TITLE = "Đọc văn bản đính kèm (PDF / Word / Excel)"
FILETYPES = [
    ("Tài liệu", "*.pdf *.docx *.xlsx *.xls"),
    ("PDF", "*.pdf"),
    ("Word", "*.docx"),
    ("Excel", "*.xlsx *.xls"),
    ("Tất cả", "*.*"),
]


class ExportApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("640x420")
        self.minsize(560, 380)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.layout = tk.StringVar(value="text")
        self.pages = tk.StringVar(value="")
        self.status = tk.StringVar(value="Chọn file để bắt đầu.")
        self._busy = False

        self._build_ui()

    # --- UI ---

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)

        self._row_file_picker(root, 0, "File nguồn", self.input_path, self._pick_input)
        self._row_file_picker(
            root,
            2,
            "File xuất (để trống = cùng tên nguồn)",
            self.output_path,
            self._pick_output,
        )
        self._row_options(root, 4)

        self.progress = ttk.Progressbar(root, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=2, sticky="ew", padx=12, pady=8)

        ttk.Label(root, textvariable=self.status, wraplength=580).grid(
            row=6, column=0, columnspan=2, sticky="w", padx=12
        )

        btns = ttk.Frame(root)
        btns.grid(row=7, column=0, columnspan=2, pady=12)
        self.run_btn = ttk.Button(btns, text="Xuất file", command=self._start_export)
        self.run_btn.pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Thoát", command=self.destroy).pack(side=tk.LEFT, padx=6)

    def _row_file_picker(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        var: tk.StringVar,
        command,
    ) -> None:
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", padx=12, pady=(6, 0)
        )
        ttk.Entry(parent, textvariable=var).grid(
            row=row + 1, column=0, sticky="ew", padx=12
        )
        btn_text = "Chọn file…" if "nguồn" in label.lower() else "Chọn nơi lưu…"
        ttk.Button(parent, text=btn_text, command=command).grid(
            row=row + 1, column=1, padx=8
        )

    def _row_options(self, parent: ttk.Frame, row: int) -> None:
        box = ttk.LabelFrame(parent, text="Tuỳ chọn", padding=10)
        box.grid(row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=10)

        ttk.Label(box, text="Layout DOCX:").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            box, text="Text (OCR, sửa được)", variable=self.layout, value="text"
        ).grid(row=0, column=1, sticky="w", padx=8)
        ttk.Radiobutton(
            box,
            text="Visual (ảnh trang, giống scan)",
            variable=self.layout,
            value="visual",
        ).grid(row=0, column=2, sticky="w", padx=8)

        ttk.Label(box, text="Số trang tối đa (PDF, trống = hết):").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(box, textvariable=self.pages, width=8).grid(
            row=1, column=1, sticky="w", padx=8, pady=(8, 0)
        )

    # --- dialogs ---

    def _pick_input(self) -> None:
        path = filedialog.askopenfilename(title="Chọn file", filetypes=FILETYPES)
        if not path:
            return
        self.input_path.set(path)
        if not self.output_path.get().strip():
            self.output_path.set(str(Path(path).with_suffix(".docx")))

    def _pick_output(self) -> None:
        """
        Chọn nơi lưu. Trên Linux, defaultextension=".docx" luôn đè đuôi
        dù đã chọn filter Text — nên gắn đuôi theo typevariable.
        """
        type_var = tk.StringVar()
        initial = self.output_path.get().strip() or self.input_path.get().strip()
        path = filedialog.asksaveasfilename(
            title="Lưu thành",
            initialfile=Path(initial).name if initial else "",
            # Để trống: không ép .docx khi user chọn Text
            defaultextension="",
            filetypes=[
                ("Word", "*.docx"),
                ("Text", "*.txt"),
                ("Tất cả", "*.*"),
            ],
            typevariable=type_var,
        )
        if not path:
            return

        out = Path(path)
        selected = type_var.get().lower()
        # typevariable có thể là "Text", "*.txt", "Word", "*.docx"...
        if "txt" in selected or selected == "text":
            want = ".txt"
        elif "docx" in selected or selected == "word":
            want = ".docx"
        else:
            # Không rõ filter: giữ đuôi user gõ, mặc định .docx
            want = out.suffix.lower() if out.suffix else ".docx"

        if out.suffix.lower() != want:
            out = out.with_suffix(want)
        self.output_path.set(str(out))

    # --- export ---

    def _parse_pages(self) -> int | None:
        raw = self.pages.get().strip()
        if not raw:
            return None
        n = int(raw)
        if n < 1:
            raise ValueError("Số trang phải ≥ 1")
        return n

    def _start_export(self) -> None:
        if self._busy:
            return

        src = self.input_path.get().strip()
        if not src:
            messagebox.showwarning(APP_TITLE, "Hãy chọn file nguồn.")
            return
        if not Path(src).is_file():
            messagebox.showerror(APP_TITLE, f"Không tìm thấy file:\n{src}")
            return

        try:
            max_pages = self._parse_pages()
        except ValueError as exc:
            messagebox.showerror(APP_TITLE, str(exc))
            return

        layout = self.layout.get()
        if layout == "visual" and Path(src).suffix.lower() != ".pdf":
            messagebox.showerror(APP_TITLE, "Layout Visual chỉ dùng với file PDF.")
            return

        out = self.output_path.get().strip() or None
        self._set_busy(True)
        self.status.set("Đang xử lý…")

        def worker() -> None:
            err: Exception | None = None
            result: Path | None = None

            def on_progress(cur: int, total: int) -> None:
                self.after(0, lambda c=cur, t=total: self._on_progress(c, t))

            try:
                result = export_attachment(
                    src,
                    out,
                    use_ocr=True,
                    max_pages=max_pages,
                    progress=on_progress,
                    layout=layout,
                )
            except Exception as exc:  # noqa: BLE001
                err = exc

            self.after(0, lambda: self._on_done(result, err))

        threading.Thread(target=worker, daemon=True).start()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.run_btn.configure(state=tk.DISABLED if busy else tk.NORMAL)
        if busy:
            self.progress.configure(value=0, maximum=100)

    def _on_progress(self, cur: int, total: int) -> None:
        self.progress.configure(maximum=max(total, 1), value=cur)
        label = "Render" if self.layout.get() == "visual" else "OCR"
        self.status.set(f"{label} trang {cur}/{total}…")

    def _on_done(self, result: Path | None, err: Exception | None) -> None:
        self._set_busy(False)
        if err is not None:
            self.status.set("Lỗi.")
            messagebox.showerror(APP_TITLE, str(err))
            return
        if result is None:
            self.status.set("Không đọc được nội dung.")
            messagebox.showwarning(
                APP_TITLE, "File không có text có thể đọc được."
            )
            return
        self.progress.configure(value=self.progress["maximum"])
        self.status.set(f"Xong: {result}")
        self.output_path.set(str(result))
        messagebox.showinfo(APP_TITLE, f"Đã ghi:\n{result}")


def main() -> None:
    try:
        app = ExportApp()
    except tk.TclError as exc:
        print(
            "Không khởi tạo được Tkinter.\n"
            "  Ubuntu/Debian: sudo apt install python3-tk\n"
            "  Fedora:        sudo dnf install python3-tkinter\n"
            "  Windows:       cài Python từ python.org (tick tcl/tk)\n"
            f"Chi tiết: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)
    app.mainloop()


if __name__ == "__main__":
    main()
