# Setup — giống React (`npm install` → không commit `node_modules`)

| React | Project này |
|-------|-------------|
| `package.json` | `requirements.txt` |
| `node_modules/` (không commit) | `.venv/` / `.packages/` / `.ocr-env/` (không commit) |
| `npm install` | `./install.sh` hoặc `install.bat` |

## Cấu trúc commit lên Git

```
app.py
index.py
doc_tool/
data/                 # từ điển Việt (nhẹ, cần commit)
requirements.txt
install.sh / install.bat
run_ui.sh / run_ui.bat
SETUP.md
.gitignore
```

**Không commit:** `.packages/`, `.ocr-env/`, `.venv/`, `.mamba/`

---

## Máy mới — Ubuntu

```bash
sudo apt install python3 python3-pip python3-venv python3-tk \
  tesseract-ocr tesseract-ocr-vie tesseract-ocr-eng

git clone <repo>
cd <repo>
chmod +x install.sh run_ui.sh
./install.sh

source .venv/bin/activate
python app.py
```

---

## Máy mới — Windows

1. **Python** — https://www.python.org — tick **Add to PATH** + **tcl/tk**
2. **Tesseract + Vietnamese** — https://github.com/UB-Mannheim/tesseract/wiki
3. Clone/copy repo (không cần `.ocr-env` / `.packages`)
  Install git 
    https://git-scm.com/install/windows
    Git for Windows/x64 Setup.
  Clone repo
    git clone https://github.com/macan-gdk/python.git
  
4. Chạy:
   ```bat
   install.bat
   .venv\Scripts\activate
   python app.py
   ```
   hoặc double-click `run_ui.bat` (sẽ pip nếu thiếu)

---

## Dev trên Ubuntu (máy đang code)

```bash
./install.sh          # lần đầu / khi đổi requirements.txt
source .venv/bin/activate
python app.py
```

Nếu còn `.ocr-env` cũ vẫn dùng được; máy mới chỉ cần `apt install tesseract-ocr-vie`.

---

## Cấu trúc code

```
doc_tool/           # core
  bootstrap.py
  tesseract_env.py
  viet_correct.py
  readers.py
  export.py
  cli.py
app.py              # UI
index.py            # facade CLI
```
