# PDF Tools

A desktop application for common PDF operations, built with Python and PySide6. Clean dark UI with a tabbed interface — no cloud, no subscription, no data sent anywhere.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

| Tab | What it does |
|---|---|
| **Merge** | Combine multiple PDFs into one. Drag and drop to reorder before merging. |
| **Split** | Split a PDF into individual pages or custom page ranges (e.g. `1-3, 5-8`). |
| **Rotate** | Rotate all pages or specific pages by 90°, 180°, or 270°. |
| **Security** | Encrypt a PDF with user/owner passwords, or remove an existing password. |
| **Compress** | Reduce file size using Ghostscript with four quality profiles. |
| **Info / Metadata** | View all metadata fields of a PDF and edit them freely. |

---

## Screenshots

> _Add screenshots here after cloning the repo._

---

## Requirements

- Python 3.10 or higher
- [PySide6](https://pypi.org/project/PySide6/)
- [pypdf](https://pypi.org/project/pypdf/)
- [Ghostscript](https://ghostscript.com/releases/gsdnld.html) _(optional — required for the Compress tab only)_

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/pdf-tools.git
cd pdf-tools
```

**2. Create and activate a virtual environment** _(recommended)_

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install PySide6 pypdf
```

**4. (Optional) Install Ghostscript for compression**

Download the installer from https://ghostscript.com/releases/gsdnld.html and make sure it is added to your system PATH. On Windows, select **"Add to PATH"** during installation.

**5. Run the application**

```bash
python main.py
```

---

## Usage

### Merge

1. Go to the **Merge** tab.
2. Click **＋ Add** or drag PDF files directly onto the list.
3. Reorder files by dragging them within the list, or use the **▲ Up / ▼ Down** buttons.
4. Click **Save as…** to choose the output file path.
5. Click **⧉ Merge PDFs**.

---

### Split

1. Go to the **Split** tab.
2. Click **Select PDF…** to choose the input file.
3. Choose a split mode:
   - **One page per file** — creates one PDF per page.
   - **Page ranges** — enter ranges like `1-3, 5-8, 10-12` to create one PDF per range.
4. Click **Select folder…** to choose where the output files will be saved.
5. Click **✂ Split PDF**.

---

### Rotate

1. Go to the **Rotate** tab.
2. Click **Select PDF…** to choose the input file.
3. Select the rotation angle: 90° (clockwise), 180°, or 270° (counter-clockwise).
4. In the **Pages** field, enter specific pages or ranges (e.g. `1, 3, 5-8`). Leave blank to rotate all pages.
5. Click **Save as…** and then **↻ Rotate**.

---

### Security

**Encrypt a PDF**

1. Go to the **Security** tab.
2. Under **Encrypt PDF**, select the input file.
3. Enter a **user password** (required to open the PDF).
4. Optionally enter an **owner password** (restricts editing and printing).
5. Choose an output file and click **🔒 Encrypt**.

**Remove a password**

1. Under **Decrypt PDF**, select the encrypted file.
2. Enter the current password.
3. Choose an output file and click **🔓 Decrypt**.

---

### Compress

> Requires Ghostscript installed and available in PATH.

1. Go to the **Compress** tab.
2. Select the input PDF.
3. Choose a compression profile:
   - **screen** — smallest file size, 72 dpi, suitable for web/email.
   - **ebook** — balanced quality and size, 150 dpi.
   - **printer** — high quality, 300 dpi.
   - **prepress** — maximum quality with color preservation, 300 dpi.
4. Choose an output file and click **⚙ Compress**. The log will show the original vs compressed size and the reduction percentage.

---

### Info / Metadata

1. Go to the **Info / Metadata** tab.
2. Click **Select PDF…** — all available metadata fields are loaded automatically into both the **File Information** section (read-only) and the **Edit Metadata** section.
3. Edit any fields you want to update (Title, Author, Subject, Keywords, Creator, Producer, etc.).
4. Click **Save as…** to choose the output file.
5. Click **💾 Save Metadata**.

Any non-standard metadata keys found in the file are reported in the Output log.

---

## Output Log

All operations write progress messages and errors to the **OUTPUT / LOG** panel at the bottom of the window. Click **Clear log** to reset it.

---

## Icon

Place a file named `icone.ico` in the same directory as `main.py` to use a custom window icon.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

Developed by **Fernando Valverde**
