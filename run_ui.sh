#!/usr/bin/env bash
# Chạy UI — ưu tiên .venv nếu có
cd "$(dirname "$0")"

if [ -f .venv/bin/python ]; then
  PY=.venv/bin/python
else
  PY=python3
fi

if ! "$PY" -c "import tkinter" 2>/dev/null; then
  echo "Thiếu tkinter. Cài: sudo apt install python3-tk"
  exit 1
fi

if ! "$PY" -c "import doc_tool" 2>/dev/null; then
  echo "Chưa cài deps. Chạy: ./install.sh"
  exit 1
fi

exec "$PY" app.py
