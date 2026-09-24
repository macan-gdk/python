#!/usr/bin/env bash
# Giống npm install: cài Python deps vào .venv (khuyến nghị) hoặc --user
set -e
cd "$(dirname "$0")"

echo "==> Kiểm tra Python..."
if ! command -v python3 >/dev/null; then
  echo "Thiếu python3. Ubuntu: sudo apt install python3 python3-pip python3-venv python3-tk"
  exit 1
fi

echo "==> Tạo / dùng .venv..."
if [ ! -d .venv ]; then
  python3 -m venv .venv 2>/dev/null || {
    echo "venv lỗi — thử: sudo apt install python3-venv"
    echo "Hoặc cài user: python3 -m pip install --user -r requirements.txt"
    python3 -m pip install --user -r requirements.txt
    echo "Xong (user install)."
    exit 0
  }
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ""
echo "==> Tesseract (OCR tiếng Việt) — hệ thống:"
if command -v tesseract >/dev/null; then
  tesseract --list-langs 2>/dev/null | head -20 || true
else
  echo "  Chưa có tesseract. Cài:"
  echo "    sudo apt install tesseract-ocr tesseract-ocr-vie tesseract-ocr-eng"
fi

echo ""
echo "Xong. Chạy UI:"
echo "  source .venv/bin/activate && python app.py"
echo "  hoặc: ./run_ui.sh"
