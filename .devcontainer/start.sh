#!/bin/bash
echo "Arty başlatılıyor..."

cd /workspaces/artyai

if [ ! -f .env ]; then
  cp .env.example .env
  echo "UYARI: .env dosyası oluşturuldu, API key ekle!"
fi

set -a
source /workspaces/artyai/.env
set +a

pkill -f uvicorn 2>/dev/null || true
sleep 1

nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /workspaces/artyai/arty.log 2>&1 &
sleep 2
echo "Arty çalışıyor → port 8000"
echo "Log: tail -f /workspaces/artyai/arty.log"
