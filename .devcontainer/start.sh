#!/bin/bash
echo "Arty başlatılıyor..."

# .env yoksa oluştur
if [ ! -f .env ]; then
  cp .env.example .env
fi

# Arka planda çalıştır, log yaz
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > arty.log 2>&1 &
echo "Arty çalışıyor → port 8000"
echo "Log: tail -f arty.log"
