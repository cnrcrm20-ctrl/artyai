# ArtyAI

Kişisel yapay zeka agent. FastAPI + OpenRouter multi-model.

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
# .env dosyasına OpenRouter API key yaz
```

## Çalıştır

```bash
uvicorn main:app --reload
```

## CLI

```bash
python interfaces/cli.py
```

## API

- `POST /chat` — mesaj gönder
- `GET /history/{session_id}` — geçmiş
- `POST /memory/fact` — gerçek kaydet
- `GET /memory/facts` — tüm gerçekler
- `GET /health` — durum

## Modeller (Free)

| Görev | Model |
|-------|-------|
| Sohbet | Llama 3.3 70B |
| Kod | DeepSeek R1 |
| Arama | Gemini Flash |
| Hızlı | Llama 3.1 8B |
