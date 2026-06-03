"""
PDF Tools — Developed by Fernando Valverde
Requires: pip install PySide6 pypdf
Optional:  ghostscript (in PATH) for compression
"""

import sys
import os
import shutil
import subprocess

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QFileDialog, QLabel,
    QTextEdit, QFrame, QAbstractItemView, QSizePolicy, QTabWidget,
    QLineEdit, QFormLayout, QComboBox, QGroupBox, QProgressBar,
    QCheckBox, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon

try:
    from pypdf import PdfWriter, PdfReader
    PYPDF_OK = True
except ImportError:
    PYPDF_OK = False


# ═══════════════════════════════════════════════════════════════════════════════
#  THEME
# ═══════════════════════════════════════════════════════════════════════════════

STYLE = """
QMainWindow, QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}
QTabWidget::pane {
    border: 1px solid #313244;
    border-radius: 8px;
    background: #181825;
}
QTabBar::tab {
    background: #313244; color: #a6adc8;
    padding: 8px 18px; border-top-left-radius: 6px;
    border-top-right-radius: 6px; margin-right: 3px;
    font-weight: bold; font-size: 12px;
}
QTabBar::tab:selected  { background: #cba6f7; color: #1e1e2e; }
QTabBar::tab:hover:!selected { background: #45475a; color: #cdd6f4; }
QPushButton {
    background-color: #313244; color: #cdd6f4;
    border: 1px solid #45475a; border-radius: 6px; padding: 7px 16px;
}
QPushButton:hover   { background-color: #45475a; border-color: #7f849c; }
QPushButton:pressed { background-color: #585b70; }
QPushButton:disabled { background-color: #1e1e2e; color: #45475a; border-color: #313244; }
QPushButton#primary {
    background-color: #cba6f7; color: #1e1e2e;
    font-weight: bold; font-size: 14px; border: none; padding: 9px 24px; border-radius: 7px;
}
QPushButton#primary:hover   { background-color: #d6b8ff; }
QPushButton#primary:pressed { background-color: #b891f5; }
QPushButton#primary:disabled { background-color: #45475a; color: #585b70; }
QPushButton#danger { background-color: #313244; color: #f38ba8; border: 1px solid #f38ba8; }
QPushButton#danger:hover { background-color: #f38ba8; color: #1e1e2e; }
QPushButton#warn   { background-color: #313244; color: #fab387; border: 1px solid #fab387; }
QPushButton#warn:hover   { background-color: #fab387; color: #1e1e2e; }
QPushButton#green  { background-color: #313244; color: #a6e3a1; border: 1px solid #a6e3a1; }
QPushButton#green:hover  { background-color: #a6e3a1; color: #1e1e2e; }
QListWidget {
    background-color: #11111b; border: 1px solid #313244;
    border-radius: 8px; padding: 4px; color: #cdd6f4;
    selection-background-color: #45475a;
}
QListWidget::item { padding: 6px 8px; border-radius: 4px; }
QListWidget::item:alternate { background-color: #1e1e2e; }
QListWidget::item:selected  { background-color: #45475a; color: #cba6f7; }
QListWidget::item:hover:!selected { background-color: #2a2a3c; }
QTextEdit, QLineEdit {
    background-color: #11111b; border: 1px solid #313244;
    border-radius: 6px; padding: 6px; color: #cdd6f4;
}
QTextEdit#console {
    color: #a6e3a1;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
}
QLineEdit:focus, QTextEdit:focus { border-color: #cba6f7; }
QComboBox {
    background-color: #313244; border: 1px solid #45475a;
    border-radius: 6px; padding: 5px 10px; color: #cdd6f4;
}
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background-color: #313244; color: #cdd6f4;
    selection-background-color: #45475a; border: 1px solid #585b70;
}
QGroupBox {
    border: 1px solid #313244; border-radius: 8px;
    margin-top: 10px; padding: 10px; color: #a6adc8;
    font-size: 11px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }
QLabel#section { font-size: 11px; font-weight: bold; color: #a6adc8; letter-spacing: 1px; }
QLabel#hint    { font-size: 11px; color: #585b70; font-style: italic; }
QLabel#title   { font-size: 22px; font-weight: bold; color: #cba6f7; padding: 4px 0; }
QLabel#footer  { font-size: 11px; color: #585b70; padding: 4px 0; }
QLabel#meta_value { color: #89dceb; font-size: 12px; }
QFrame#divider { color: #313244; }
QCheckBox { color: #cdd6f4; spacing: 6px; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid #45475a; border-radius: 3px; background: #313244;
}
QCheckBox::indicator:checked { background-color: #cba6f7; border-color: #cba6f7; }
QProgressBar {
    background: #313244; border: 1px solid #45475a;
    border-radius: 6px; height: 8px; text-align: center; color: transparent;
}
QProgressBar::chunk { background: #cba6f7; border-radius: 5px; }
QScrollArea { border: none; background: transparent; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical   { background: #181825; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #45475a; border-radius: 5px; min-height: 20px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal  { background: #181825; height: 10px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #45475a; border-radius: 5px; min-width: 20px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  WORKERS
# ═══════════════════════════════════════════════════════════════════════════════

class BaseWorker(QThread):
    log      = Signal(str)
    err      = Signal(str)
    progress = Signal(int)
    finished = Signal(bool, str)


class MergeWorker(BaseWorker):
    def __init__(self, paths, output):
        super().__init__(); self.paths = paths; self.output = output

    def run(self):
        try:
            w = PdfWriter(); total = 0
            for i, p in enumerate(self.paths, 1):
                self.log.emit(f"[{i}/{len(self.paths)}] {os.path.basename(p)}")
                r = PdfReader(p)
                for pg in r.pages: w.add_page(pg)
                total += len(r.pages)
                self.progress.emit(int(i / len(self.paths) * 100))
            self.log.emit(f"Saving → {self.output}")
            with open(self.output, "wb") as f: w.write(f)
            self.log.emit(f"✔ Done! {total} pages from {len(self.paths)} file(s).")
            self.finished.emit(True, self.output)
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


class SplitWorker(BaseWorker):
    def __init__(self, path, output_dir, mode, ranges):
        super().__init__()
        self.path = path; self.output_dir = output_dir
        self.mode = mode; self.ranges = ranges

    def run(self):
        try:
            r = PdfReader(self.path); total = len(r.pages)
            base = os.path.splitext(os.path.basename(self.path))[0]
            if self.mode == "all":
                for i, pg in enumerate(r.pages, 1):
                    w = PdfWriter(); w.add_page(pg)
                    out = os.path.join(self.output_dir, f"{base}_p{i:04d}.pdf")
                    with open(out, "wb") as f: w.write(f)
                    self.progress.emit(int(i / total * 100))
                self.log.emit(f"✔ {total} file(s) created in {self.output_dir}")
            else:
                for idx, (s, e) in enumerate(self.ranges, 1):
                    s = max(1, min(s, total)); e = max(s, min(e, total))
                    w = PdfWriter()
                    for pi in range(s-1, e): w.add_page(r.pages[pi])
                    out = os.path.join(self.output_dir, f"{base}_p{s}-{e}.pdf")
                    with open(out, "wb") as f: w.write(f)
                    self.log.emit(f"  {s}–{e} → {os.path.basename(out)}")
                    self.progress.emit(int(idx / len(self.ranges) * 100))
                self.log.emit(f"✔ {len(self.ranges)} file(s) created.")
            self.finished.emit(True, self.output_dir)
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


class RotateWorker(BaseWorker):
    def __init__(self, path, output, angle, pages):
        super().__init__()
        self.path = path; self.output = output; self.angle = angle; self.pages = pages

    def run(self):
        try:
            r = PdfReader(self.path); w = PdfWriter(); total = len(r.pages)
            for i, pg in enumerate(r.pages, 1):
                if not self.pages or i in self.pages: pg.rotate(self.angle)
                w.add_page(pg); self.progress.emit(int(i / total * 100))
            with open(self.output, "wb") as f: w.write(f)
            self.log.emit(f"✔ {self.angle}° rotation applied → {self.output}")
            self.finished.emit(True, self.output)
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


class EncryptWorker(BaseWorker):
    def __init__(self, path, output, user_pw, owner_pw):
        super().__init__()
        self.path = path; self.output = output
        self.user_pw = user_pw; self.owner_pw = owner_pw

    def run(self):
        try:
            r = PdfReader(self.path); w = PdfWriter()
            for pg in r.pages: w.add_page(pg)
            w.encrypt(self.user_pw, self.owner_pw or None)
            with open(self.output, "wb") as f: w.write(f)
            self.log.emit(f"✔ PDF encrypted → {self.output}")
            self.finished.emit(True, self.output)
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


class DecryptWorker(BaseWorker):
    def __init__(self, path, output, password):
        super().__init__()
        self.path = path; self.output = output; self.password = password

    def run(self):
        try:
            r = PdfReader(self.path)
            if r.is_encrypted:
                if r.decrypt(self.password) == 0:
                    self.err.emit("✖ Wrong password."); self.finished.emit(False, "Wrong password"); return
            w = PdfWriter()
            for pg in r.pages: w.add_page(pg)
            with open(self.output, "wb") as f: w.write(f)
            self.log.emit(f"✔ PDF decrypted → {self.output}")
            self.finished.emit(True, self.output)
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


class CompressWorker(BaseWorker):
    def __init__(self, path, output, profile):
        super().__init__()
        self.path = path; self.output = output; self.profile = profile

    def run(self):
        gs = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
        if not gs:
            self.err.emit("✖ Ghostscript not found in PATH.")
            self.finished.emit(False, "ghostscript missing"); return
        cmd = [gs, "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dBATCH", "-dQUIET",
               f"-dPDFSETTINGS=/{self.profile}", f"-sOutputFile={self.output}", self.path]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            orig = os.path.getsize(self.path); comp = os.path.getsize(self.output)
            pct = (1 - comp / orig) * 100 if orig else 0
            self.log.emit(f"✔ {orig/1024:.1f} KB → {comp/1024:.1f} KB  ({pct:.1f}% smaller)")
            self.finished.emit(True, self.output)
        except subprocess.CalledProcessError as e:
            self.err.emit(f"✖ GS error: {e.stderr.decode(errors='replace')}"); self.finished.emit(False, str(e))
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


class MetaWorker(BaseWorker):
    def __init__(self, path, output, meta):
        super().__init__()
        self.path = path; self.output = output; self.meta = meta

    def run(self):
        try:
            r = PdfReader(self.path); w = PdfWriter()
            for pg in r.pages: w.add_page(pg)
            w.add_metadata(self.meta)
            with open(self.output, "wb") as f: w.write(f)
            self.log.emit("✔ Metadata saved.")
            self.finished.emit(True, self.output)
        except Exception as e:
            self.err.emit(f"✖ {e}"); self.finished.emit(False, str(e))


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class DragDropList(QListWidget):
    files_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True); self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(True); self.setSpacing(2)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            pdfs = [u.toLocalFile() for u in e.mimeData().urls()
                    if u.toLocalFile().lower().endswith(".pdf")]
            if pdfs: e.acceptProposedAction(); return
        super().dragEnterEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()
        else: super().dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            pdfs = [u.toLocalFile() for u in e.mimeData().urls()
                    if u.toLocalFile().lower().endswith(".pdf")]
            if pdfs: self.files_dropped.emit(pdfs); e.acceptProposedAction(); return
        super().dropEvent(e)


def divider():
    f = QFrame(); f.setObjectName("divider"); f.setFrameShape(QFrame.Shape.HLine); return f

def slabel(text):
    l = QLabel(text); l.setObjectName("section"); return l

def hlabel(text):
    l = QLabel(text); l.setObjectName("hint"); return l

def pick_pdf(parent, title="Select PDF"):
    p, _ = QFileDialog.getOpenFileName(parent, title, "", "PDF Files (*.pdf)"); return p

def save_pdf(parent, default="output.pdf"):
    p, _ = QFileDialog.getSaveFileName(parent, "Save as", default, "PDF Files (*.pdf)")
    if p and not p.lower().endswith(".pdf"): p += ".pdf"
    return p

def pick_dir(parent):
    return QFileDialog.getExistingDirectory(parent, "Select output folder")

def exl(widget):
    widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    return widget


class Console(QTextEdit):
    def __init__(self):
        super().__init__(); self.setObjectName("console")
        self.setReadOnly(True); self.setMinimumHeight(110)

    def _scroll(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def log(self, m): self.append(m); self._scroll()
    def err(self, m): self.append(f'<span style="color:#f38ba8;">{m}</span>'); self._scroll()
    def info(self, m): self.append(f'<span style="color:#89b4fa;">{m}</span>'); self._scroll()
    def ok(self, m): self.append(f'<span style="color:#a6e3a1;">{m}</span>'); self._scroll()


# ═══════════════════════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════════════════════

# ── MERGE ─────────────────────────────────────────────────────────────────────

class MergeTab(QWidget):
    def __init__(self, con: Console):
        super().__init__(); self.con = con; self.out = ""; self.worker = None; self._ui()

    def _ui(self):
        L = QVBoxLayout(self); L.setContentsMargins(14,14,14,14); L.setSpacing(10)
        L.addWidget(hlabel("Add PDFs, drag to reorder, then click Merge."))
        self.lst = DragDropList(); self.lst.files_dropped.connect(self._add)
        L.addWidget(self.lst, stretch=1)

        br = QHBoxLayout(); br.setSpacing(6)
        for txt, fn, obj in [("＋ Add", self._browse, ""), ("▲ Up", self._up, ""),
                              ("▼ Down", self._down, ""), ("✖ Remove", self._rem, "danger"),
                              ("🗑 Clear all", self._clr, "warn")]:
            b = QPushButton(txt); b.clicked.connect(fn)
            if obj: b.setObjectName(obj)
            br.addWidget(b)
        br.addStretch(); L.addLayout(br); L.addWidget(divider())

        mr = QHBoxLayout(); mr.setSpacing(8)
        mr.addWidget(slabel("OUTPUT:"))
        self.lbl = exl(hlabel("(no file selected)")); mr.addWidget(self.lbl, stretch=1)
        bs = QPushButton("Save as…"); bs.clicked.connect(self._out); mr.addWidget(bs)
        self.btn = QPushButton("⧉  Merge PDFs"); self.btn.setObjectName("primary")
        self.btn.setEnabled(False); self.btn.clicked.connect(self._run); mr.addWidget(self.btn)
        L.addLayout(mr)
        self.pb = QProgressBar(); self.pb.setVisible(False); L.addWidget(self.pb)

    def _browse(self):
        ps, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")
        if ps: self._add(ps)

    def _add(self, paths):
        ex = {self.lst.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.lst.count())}
        n = 0
        for p in paths:
            if p not in ex:
                it = QListWidgetItem(f"  📄  {os.path.basename(p)}")
                it.setData(Qt.ItemDataRole.UserRole, p); it.setToolTip(p)
                self.lst.addItem(it); ex.add(p); n += 1
        if n: self.con.log(f"+ {n} file(s) added.")
        self._ref()

    def _up(self):
        r = self.lst.currentRow()
        if r > 0:
            it = self.lst.takeItem(r); self.lst.insertItem(r-1, it); self.lst.setCurrentRow(r-1)

    def _down(self):
        r = self.lst.currentRow()
        if r < self.lst.count()-1:
            it = self.lst.takeItem(r); self.lst.insertItem(r+1, it); self.lst.setCurrentRow(r+1)

    def _rem(self):
        for it in self.lst.selectedItems(): self.lst.takeItem(self.lst.row(it))
        self._ref()

    def _clr(self):
        self.lst.clear(); self.con.log("List cleared."); self._ref()

    def _out(self):
        p = save_pdf(self, "merged.pdf")
        if p: self.out = p; self.lbl.setText(p); self._ref()

    def _ref(self):
        self.btn.setEnabled(PYPDF_OK and self.lst.count() >= 2 and bool(self.out))

    def _run(self):
        paths = [self.lst.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.lst.count())]
        self.con.info(f"\n── Merging {len(paths)} file(s) ──")
        self.btn.setEnabled(False); self.btn.setText("Processing…")
        self.pb.setValue(0); self.pb.setVisible(True)
        self.worker = MergeWorker(paths, self.out)
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.progress.connect(self.pb.setValue); self.worker.finished.connect(self._done)
        self.worker.start()

    def _done(self, ok, info):
        self.btn.setText("⧉  Merge PDFs"); self._ref(); self.pb.setVisible(False)
        (self.con.ok if ok else self.con.err)(f"{'✔ Saved' if ok else '✖ Failed'}: {info}\n")


# ── SPLIT ─────────────────────────────────────────────────────────────────────

class SplitTab(QWidget):
    def __init__(self, con: Console):
        super().__init__(); self.con = con; self.src = ""; self.outd = ""; self.worker = None; self._ui()

    def _ui(self):
        L = QVBoxLayout(self); L.setContentsMargins(14,14,14,14); L.setSpacing(10)

        g1 = QGroupBox("Input file"); h1 = QHBoxLayout(g1)
        self.lbl_s = exl(hlabel("(none)")); b1 = QPushButton("Select PDF…"); b1.clicked.connect(self._pick_s)
        h1.addWidget(self.lbl_s, stretch=1); h1.addWidget(b1); L.addWidget(g1)

        g2 = QGroupBox("Split mode"); m2 = QVBoxLayout(g2)
        self.cb_all = QCheckBox("One page per file (split all pages)")
        self.cb_all.setChecked(True)
        self.cb_all.toggled.connect(lambda c: self.ed_r.setEnabled(not c))
        m2.addWidget(self.cb_all)
        rh = QHBoxLayout(); rh.addWidget(hlabel("Page ranges (e.g. 1-3, 5-8):"))
        self.ed_r = QLineEdit(); self.ed_r.setPlaceholderText("1-3, 5-8"); self.ed_r.setEnabled(False)
        rh.addWidget(self.ed_r, stretch=1); m2.addLayout(rh); L.addWidget(g2)

        g3 = QGroupBox("Output folder"); h3 = QHBoxLayout(g3)
        self.lbl_d = exl(hlabel("(none)")); b3 = QPushButton("Select folder…"); b3.clicked.connect(self._pick_d)
        h3.addWidget(self.lbl_d, stretch=1); h3.addWidget(b3); L.addWidget(g3)

        L.addStretch()
        br = QHBoxLayout(); br.addStretch()
        self.btn = QPushButton("✂  Split PDF"); self.btn.setObjectName("primary")
        self.btn.setEnabled(False); self.btn.clicked.connect(self._run); br.addWidget(self.btn)
        L.addLayout(br)
        self.pb = QProgressBar(); self.pb.setVisible(False); L.addWidget(self.pb)

    def _pick_s(self):
        p = pick_pdf(self)
        if p: self.src = p; self.lbl_s.setText(os.path.basename(p)); self._ref()

    def _pick_d(self):
        d = pick_dir(self)
        if d: self.outd = d; self.lbl_d.setText(d); self._ref()

    def _ref(self): self.btn.setEnabled(bool(self.src and self.outd))

    def _parse_r(self):
        res = []
        for part in self.ed_r.text().split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-", 1)
                try: res.append((int(a.strip()), int(b.strip())))
                except: pass
        return res

    def _run(self):
        if self.cb_all.isChecked():
            mode, ranges = "all", []
        else:
            ranges = self._parse_r()
            if not ranges: self.con.err("✖ No valid ranges. Example: 1-3, 5-8"); return
            mode = "ranges"
        self.con.info(f"\n── Splitting: {os.path.basename(self.src)} ──")
        self.btn.setEnabled(False); self.btn.setText("Processing…")
        self.pb.setValue(0); self.pb.setVisible(True)
        self.worker = SplitWorker(self.src, self.outd, mode, ranges)
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.progress.connect(self.pb.setValue); self.worker.finished.connect(self._done)
        self.worker.start()

    def _done(self, ok, info):
        self.btn.setText("✂  Split PDF"); self._ref(); self.pb.setVisible(False)
        (self.con.ok if ok else self.con.err)(f"{'✔ Files saved to' if ok else '✖ Failed'}: {info}\n")


# ── ROTATE ────────────────────────────────────────────────────────────────────

class RotateTab(QWidget):
    def __init__(self, con: Console):
        super().__init__(); self.con = con; self.src = ""; self.out = ""; self.worker = None; self._ui()

    def _ui(self):
        L = QVBoxLayout(self); L.setContentsMargins(14,14,14,14); L.setSpacing(10)

        g1 = QGroupBox("Input file"); h1 = QHBoxLayout(g1)
        self.lbl_s = exl(hlabel("(none)")); b1 = QPushButton("Select PDF…"); b1.clicked.connect(self._pick)
        h1.addWidget(self.lbl_s, stretch=1); h1.addWidget(b1); L.addWidget(g1)

        g2 = QGroupBox("Settings"); f2 = QFormLayout(g2)
        self.cmb = QComboBox()
        self.cmb.addItems(["90° — clockwise", "180°", "270° — counter-clockwise"])
        f2.addRow("Angle:", self.cmb)
        self.ed_pg = QLineEdit(); self.ed_pg.setPlaceholderText("e.g. 1, 3, 5-8  (blank = all pages)")
        f2.addRow("Pages:", self.ed_pg); L.addWidget(g2)

        g3 = QGroupBox("Output file"); h3 = QHBoxLayout(g3)
        self.lbl_o = exl(hlabel("(none)")); b3 = QPushButton("Save as…"); b3.clicked.connect(self._pick_o)
        h3.addWidget(self.lbl_o, stretch=1); h3.addWidget(b3); L.addWidget(g3)

        L.addStretch()
        br = QHBoxLayout(); br.addStretch()
        self.btn = QPushButton("↻  Rotate"); self.btn.setObjectName("primary")
        self.btn.setEnabled(False); self.btn.clicked.connect(self._run); br.addWidget(self.btn)
        L.addLayout(br)
        self.pb = QProgressBar(); self.pb.setVisible(False); L.addWidget(self.pb)

    def _pick(self):
        p = pick_pdf(self)
        if p: self.src = p; self.lbl_s.setText(os.path.basename(p)); self._ref()

    def _pick_o(self):
        p = save_pdf(self, "rotated.pdf")
        if p: self.out = p; self.lbl_o.setText(p); self._ref()

    def _ref(self): self.btn.setEnabled(bool(self.src and self.out))

    def _parse_pg(self):
        txt = self.ed_pg.text().strip()
        if not txt: return set()
        pages = set()
        for part in txt.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-", 1)
                try: pages.update(range(int(a.strip()), int(b.strip())+1))
                except: pass
            else:
                try: pages.add(int(part))
                except: pass
        return pages

    def _run(self):
        angle = [90, 180, 270][self.cmb.currentIndex()]
        pages = self._parse_pg()
        self.con.info(f"\n── Rotating {angle}° ({'all pages' if not pages else str(pages)}) ──")
        self.btn.setEnabled(False); self.btn.setText("Processing…")
        self.pb.setValue(0); self.pb.setVisible(True)
        self.worker = RotateWorker(self.src, self.out, angle, pages)
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.progress.connect(self.pb.setValue); self.worker.finished.connect(self._done)
        self.worker.start()

    def _done(self, ok, info):
        self.btn.setText("↻  Rotate"); self._ref(); self.pb.setVisible(False)
        (self.con.ok if ok else self.con.err)(f"{'✔ Saved' if ok else '✖ Failed'}: {info}\n")


# ── SECURITY ──────────────────────────────────────────────────────────────────

class SecurityTab(QWidget):
    def __init__(self, con: Console):
        super().__init__(); self.con = con
        self.enc_src = ""; self.enc_out = ""
        self.dec_src = ""; self.dec_out = ""
        self.worker = None; self._ui()

    def _ui(self):
        L = QVBoxLayout(self); L.setContentsMargins(14,14,14,14); L.setSpacing(10)

        def make_row(label_text, widget):
            row = QHBoxLayout(); row.setSpacing(8)
            lbl = QLabel(label_text)
            lbl.setMinimumWidth(110); lbl.setMaximumWidth(130)
            row.addWidget(lbl); row.addWidget(widget, stretch=1)
            return row

        def make_file_row(label_text, path_label, btn):
            row = QHBoxLayout(); row.setSpacing(8)
            lbl = QLabel(label_text)
            lbl.setMinimumWidth(110); lbl.setMaximumWidth(130)
            btn.setMinimumWidth(80); btn.setMaximumWidth(90)
            path_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row.addWidget(lbl); row.addWidget(path_label, stretch=1); row.addWidget(btn)
            return row

        # ── Encrypt ──────────────────────────────────────────────────────────
        ge = QGroupBox("Encrypt PDF")
        ge_l = QVBoxLayout(ge); ge_l.setSpacing(7); ge_l.setContentsMargins(10,14,10,10)

        self.lbl_es = hlabel("(none)")
        be = QPushButton("Select…"); be.clicked.connect(self._pick_es)
        ge_l.addLayout(make_file_row("Input:", self.lbl_es, be))

        self.ed_upw = QLineEdit(); self.ed_upw.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_upw.setPlaceholderText("User password (to open the PDF)")
        ge_l.addLayout(make_row("User password:", self.ed_upw))

        self.ed_opw = QLineEdit(); self.ed_opw.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_opw.setPlaceholderText("Owner password (optional)")
        ge_l.addLayout(make_row("Owner password:", self.ed_opw))

        self.lbl_eo = hlabel("(none)")
        beo = QPushButton("Save as…"); beo.clicked.connect(self._pick_eo)
        ge_l.addLayout(make_file_row("Output:", self.lbl_eo, beo))

        self.btn_enc = QPushButton("🔒  Encrypt"); self.btn_enc.setObjectName("primary")
        self.btn_enc.setMinimumHeight(36); self.btn_enc.clicked.connect(self._run_enc)
        ge_l.addWidget(self.btn_enc)
        L.addWidget(ge)

        L.addWidget(divider())

        # ── Decrypt ──────────────────────────────────────────────────────────
        gd = QGroupBox("Decrypt PDF (remove password)")
        gd_l = QVBoxLayout(gd); gd_l.setSpacing(7); gd_l.setContentsMargins(10,14,10,10)

        self.lbl_ds = hlabel("(none)")
        bd = QPushButton("Select…"); bd.clicked.connect(self._pick_ds)
        gd_l.addLayout(make_file_row("Input:", self.lbl_ds, bd))

        self.ed_dpw = QLineEdit(); self.ed_dpw.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_dpw.setPlaceholderText("Current password")
        gd_l.addLayout(make_row("Password:", self.ed_dpw))

        self.lbl_do = hlabel("(none)")
        bdo = QPushButton("Save as…"); bdo.clicked.connect(self._pick_do)
        gd_l.addLayout(make_file_row("Output:", self.lbl_do, bdo))

        self.btn_dec = QPushButton("🔓  Decrypt"); self.btn_dec.setObjectName("green")
        self.btn_dec.setMinimumHeight(36); self.btn_dec.clicked.connect(self._run_dec)
        gd_l.addWidget(self.btn_dec)
        L.addWidget(gd); L.addStretch()

    def _pick_es(self):
        p = pick_pdf(self)
        if p: self.enc_src = p; self.lbl_es.setText(os.path.basename(p))

    def _pick_eo(self):
        p = save_pdf(self, "encrypted.pdf")
        if p: self.enc_out = p; self.lbl_eo.setText(p)

    def _pick_ds(self):
        p = pick_pdf(self)
        if p: self.dec_src = p; self.lbl_ds.setText(os.path.basename(p))

    def _pick_do(self):
        p = save_pdf(self, "decrypted.pdf")
        if p: self.dec_out = p; self.lbl_do.setText(p)

    def _run_enc(self):
        if not self.enc_src or not self.enc_out:
            self.con.err("✖ Select input and output files."); return
        if not self.ed_upw.text():
            self.con.err("✖ User password is required."); return
        self.con.info("\n── Encrypting ──")
        self.worker = EncryptWorker(self.enc_src, self.enc_out,
                                    self.ed_upw.text(), self.ed_opw.text())
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.finished.connect(lambda ok, i: self.con.ok(f"✔ {i}\n") if ok else None)
        self.worker.start()

    def _run_dec(self):
        if not self.dec_src or not self.dec_out:
            self.con.err("✖ Select input and output files."); return
        self.con.info("\n── Decrypting ──")
        self.worker = DecryptWorker(self.dec_src, self.dec_out, self.ed_dpw.text())
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.finished.connect(lambda ok, i: self.con.ok(f"✔ {i}\n") if ok else None)
        self.worker.start()


# ── COMPRESS ──────────────────────────────────────────────────────────────────

class CompressTab(QWidget):
    def __init__(self, con: Console):
        super().__init__(); self.con = con; self.src = ""; self.out = ""; self.worker = None; self._ui()

    def _ui(self):
        L = QVBoxLayout(self); L.setContentsMargins(14,14,14,14); L.setSpacing(10)

        g1 = QGroupBox("Input file"); h1 = QHBoxLayout(g1)
        self.lbl_s = exl(hlabel("(none)")); b1 = QPushButton("Select PDF…"); b1.clicked.connect(self._pick)
        h1.addWidget(self.lbl_s, stretch=1); h1.addWidget(b1); L.addWidget(g1)

        g2 = QGroupBox("Compression profile"); f2 = QFormLayout(g2)
        self.cmb = QComboBox()
        self.cmb.addItems([
            "screen   —  smallest size (72 dpi, web/screen viewing)",
            "ebook    —  balanced size/quality (150 dpi)",
            "printer  —  high quality (300 dpi)",
            "prepress —  maximum quality, color-preserved (300 dpi)"
        ])
        f2.addRow("Profile:", self.cmb)
        f2.addRow("", hlabel("Requires Ghostscript installed and in PATH (gs / gswin64c)"))
        L.addWidget(g2)

        g3 = QGroupBox("Output file"); h3 = QHBoxLayout(g3)
        self.lbl_o = exl(hlabel("(none)")); b3 = QPushButton("Save as…"); b3.clicked.connect(self._pick_o)
        h3.addWidget(self.lbl_o, stretch=1); h3.addWidget(b3); L.addWidget(g3)

        L.addStretch()
        br = QHBoxLayout(); br.addStretch()
        self.btn = QPushButton("⚙  Compress"); self.btn.setObjectName("primary")
        self.btn.setEnabled(False); self.btn.clicked.connect(self._run); br.addWidget(self.btn)
        L.addLayout(br)
        self.pb = QProgressBar(); self.pb.setRange(0, 0); self.pb.setVisible(False); L.addWidget(self.pb)

    def _pick(self):
        p = pick_pdf(self)
        if p: self.src = p; self.lbl_s.setText(os.path.basename(p)); self._ref()

    def _pick_o(self):
        p = save_pdf(self, "compressed.pdf")
        if p: self.out = p; self.lbl_o.setText(p); self._ref()

    def _ref(self): self.btn.setEnabled(bool(self.src and self.out))

    def _run(self):
        profiles = ["screen","ebook","printer","prepress"]
        profile = profiles[self.cmb.currentIndex()]
        self.con.info(f"\n── Compressing (profile: {profile}) ──")
        self.btn.setEnabled(False); self.btn.setText("Processing…"); self.pb.setVisible(True)
        self.worker = CompressWorker(self.src, self.out, profile)
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.finished.connect(self._done); self.worker.start()

    def _done(self, ok, info):
        self.btn.setText("⚙  Compress"); self._ref(); self.pb.setVisible(False)
        (self.con.ok if ok else self.con.err)(f"{'✔ Saved' if ok else '✖ Failed'}: {info}\n")


# ── INFO / METADATA ───────────────────────────────────────────────────────────

# All standard PDF metadata keys with friendly labels
META_FIELDS = [
    ("/Title",          "Title"),
    ("/Author",         "Author"),
    ("/Subject",        "Subject"),
    ("/Keywords",       "Keywords"),
    ("/Creator",        "Creator"),
    ("/Producer",       "Producer"),
    ("/CreationDate",   "Creation Date"),
    ("/ModDate",        "Modification Date"),
    ("/Trapped",        "Trapped"),
    ("/AAPL:Keywords",  "Apple Keywords"),
    ("/Company",        "Company"),
    ("/Manager",        "Manager"),
    ("/Category",       "Category"),
    ("/ContentStatus",  "Content Status"),
    ("/Identifier",     "Identifier"),
    ("/Language",       "Language"),
    ("/Revision",       "Revision"),
    ("/Version",        "Version"),
    ("/Copyright",      "Copyright"),
    ("/Description",    "Description"),
]

# Keys that are editable (write-supported by pypdf)
EDITABLE_KEYS = {
    "/Title", "/Author", "/Subject", "/Keywords",
    "/Creator", "/Producer", "/CreationDate", "/ModDate",
    "/Trapped", "/Company", "/Manager", "/Category",
    "/ContentStatus", "/Identifier", "/Language",
    "/Revision", "/Version", "/Copyright", "/Description",
}


class InfoTab(QWidget):
    def __init__(self, con: Console):
        super().__init__()
        self.con = con; self.src = ""; self.out = ""; self.worker = None
        self._info_labels = {}   # key → QLabel  (read-only display)
        self._edit_fields = {}   # key → QLineEdit (editable)
        self._ui()

    def _ui(self):
        L = QVBoxLayout(self); L.setContentsMargins(14,14,14,14); L.setSpacing(10)

        # File selector
        g1 = QGroupBox("PDF File"); h1 = QHBoxLayout(g1)
        self.lbl_s = exl(hlabel("(none)"))
        b1 = QPushButton("Select PDF…"); b1.clicked.connect(self._pick)
        h1.addWidget(self.lbl_s, stretch=1); h1.addWidget(b1); L.addWidget(g1)

        # Scrollable area holding both Info and Edit groups
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        inner = QWidget(); inner_l = QVBoxLayout(inner); inner_l.setSpacing(10)

        # ── File info (read-only) ──
        g2 = QGroupBox("File Information"); f2 = QFormLayout(g2)
        for key in ("Pages", "File size", "Encrypted"):
            lbl = QLabel("—"); lbl.setObjectName("meta_value")
            self._info_labels[key] = lbl; f2.addRow(f"{key}:", lbl)

        f2.addRow(divider())

        for key, label in META_FIELDS:
            lbl = QLabel("—"); lbl.setObjectName("meta_value")
            lbl.setWordWrap(True); lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self._info_labels[key] = lbl; f2.addRow(f"{label}:", lbl)
        inner_l.addWidget(g2)

        # ── Edit metadata ──
        g3 = QGroupBox("Edit Metadata"); f3 = QFormLayout(g3)
        for key, label in META_FIELDS:
            if key in EDITABLE_KEYS:
                ed = QLineEdit(); ed.setPlaceholderText(label)
                self._edit_fields[key] = ed; f3.addRow(f"{label}:", ed)
        inner_l.addWidget(g3)
        inner_l.addStretch()

        scroll.setWidget(inner); L.addWidget(scroll, stretch=1)

        # Output + save button
        g4 = QGroupBox("Save with new metadata"); h4 = QHBoxLayout(g4)
        self.lbl_o = exl(hlabel("(none)"))
        b_o = QPushButton("Save as…"); b_o.clicked.connect(self._pick_o)
        self.btn = QPushButton("💾  Save Metadata"); self.btn.setObjectName("primary")
        self.btn.setEnabled(False); self.btn.clicked.connect(self._run)
        h4.addWidget(self.lbl_o, stretch=1); h4.addWidget(b_o); h4.addWidget(self.btn)
        L.addWidget(g4)

    def _pick(self):
        p = pick_pdf(self)
        if not p: return
        self.src = p; self.lbl_s.setText(os.path.basename(p))
        if not PYPDF_OK: return
        try:
            r = PdfReader(p)
            sz = os.path.getsize(p)

            # Fixed file info
            self._info_labels["Pages"].setText(str(len(r.pages)))
            self._info_labels["File size"].setText(f"{sz/1024:.1f} KB  ({sz/1024/1024:.2f} MB)")
            self._info_labels["Encrypted"].setText("Yes" if r.is_encrypted else "No")

            # All metadata fields
            meta = r.metadata or {}

            # Collect ALL keys present in the file (including non-standard ones)
            all_keys_in_file = set(meta.keys())
            known_keys = {k for k, _ in META_FIELDS}

            for key, label in META_FIELDS:
                val = meta.get(key, None)
                display = str(val).strip() if val is not None else "—"
                self._info_labels[key].setText(display)
                if key in self._edit_fields:
                    self._edit_fields[key].setText("" if val is None else str(val).strip())

            # Show any extra non-standard keys in the console
            extra = all_keys_in_file - known_keys
            if extra:
                self.con.info(f"ℹ Additional metadata keys found in file:")
                for k in sorted(extra):
                    self.con.info(f"    {k} = {meta.get(k)}")

            self.con.info(f"ℹ Loaded: {os.path.basename(p)} — {len(r.pages)} page(s), {sz/1024:.1f} KB")
        except Exception as e:
            self.con.err(f"✖ Error reading PDF: {e}")
        self._ref()

    def _pick_o(self):
        p = save_pdf(self, "updated_metadata.pdf")
        if p: self.out = p; self.lbl_o.setText(p); self._ref()

    def _ref(self): self.btn.setEnabled(bool(self.src and self.out))

    def _run(self):
        meta = {}
        for key, ed in self._edit_fields.items():
            val = ed.text().strip()
            if val:
                meta[key] = val
        self.con.info("\n── Saving metadata ──")
        self.btn.setEnabled(False)
        self.worker = MetaWorker(self.src, self.out, meta)
        self.worker.log.connect(self.con.log); self.worker.err.connect(self.con.err)
        self.worker.finished.connect(self._done); self.worker.start()

    def _done(self, ok, info):
        self._ref()
        (self.con.ok if ok else self.con.err)(f"{'✔ Saved' if ok else '✖ Failed'}: {info}\n")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Tools")
        self.setMinimumSize(680, 860)
        self.resize(960, 920)
        self.setStyleSheet(STYLE)
        ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icone.ico")
        if os.path.exists(ico):
            self.setWindowIcon(QIcon(ico))
        self._build()

    def resizeEvent(self, event):
        if event.size().width() < 680:
            self.resize(680, event.size().height())
        super().resizeEvent(event)

    def _build(self):
        central = QWidget(); self.setCentralWidget(central)
        L = QVBoxLayout(central); L.setContentsMargins(18,14,18,10); L.setSpacing(10)

        t = QLabel("PDF Tools"); t.setObjectName("title"); L.addWidget(t)
        L.addWidget(divider())

        self.con = Console()

        tabs = QTabWidget()
        tabs.addTab(MergeTab(self.con),    "⧉  Merge")
        tabs.addTab(SplitTab(self.con),    "✂  Split")
        tabs.addTab(RotateTab(self.con),   "↻  Rotate")
        tabs.addTab(SecurityTab(self.con), "🔒  Security")
        tabs.addTab(CompressTab(self.con), "⚙  Compress")
        tabs.addTab(InfoTab(self.con),     "ℹ  Info / Metadata")
        L.addWidget(tabs, stretch=3)

        L.addWidget(divider())
        L.addWidget(slabel("OUTPUT / LOG"))
        L.addWidget(self.con, stretch=1)

        br = QHBoxLayout()
        b_clr = QPushButton("Clear log"); b_clr.clicked.connect(self.con.clear)
        br.addStretch(); br.addWidget(b_clr); L.addLayout(br)

        L.addWidget(divider())

        footer = QLabel("Developed by Fernando Valverde")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        L.addWidget(footer)

        if not PYPDF_OK:
            self.con.err("✖ pypdf not found. Run:  pip install pypdf")
        else:
            self.con.ok("✔ pypdf ready.")
            gs = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
            self.con.ok(f"✔ Ghostscript found: {gs}") if gs else \
            self.con.info("ℹ Ghostscript not found — Compress tab unavailable.")


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Windows taskbar icon fix — must be called before QApplication
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("fernandovalverde.pdftools.1")
    except Exception:
        pass
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
