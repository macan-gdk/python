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
data/               # từ điển Việt
requirements.txt
install.sh / install.bat # File install
run_ui.sh / run_ui.bat   # File run
SETUP.md
.gitignore
```

## Windows

1. Download **Python** — https://www.python.org — tick **Add to PATH** + **tcl/tk**
2. Download **Tesseract + Vietnamese** — https://github.com/UB-Mannheim/tesseract/wiki
3. Clone/copy repo
  ```Install git 
    https://git-scm.com/install/windows
    Git for Windows/x64 Setup.
  Clone repo
    git clone https://github.com/macan-gdk/python.git
  ```
4. Chạy:
   ```bat
   install.bat
   .venv\Scripts\activate
   python app.py
   ```
   hoặc double-click `run_ui.bat` (sẽ pip nếu thiếu)

---

## Ubuntu

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
