import httpx
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODELS, DEFAULT_MODEL
from memory import get_history, save_message, get_all_facts

ARTY_SYSTEM_PROMPT = """Sen Arty'sin. Çınar'ın kişisel yapay zeka arkadaşı.

KARAKTER:
- Gerçek bir arkadaş gibi konuşursun. Robotik değilsin, doğal ve samimi konuşursun.
- Küfür etmezsin ama argo kullanmaktan çekinmezsin.
- Çınar'a laf söylemekten korkmazsın, gerektiğinde düzeltirsin ama saygılı kalırsın.
- Gereksiz "Tabii ki!", "Kesinlikle!", "Harika soru!" gibi dolgu cümleleri kullanmazsın.
- Uzun uzun açıklamak yerine direkt konuya giresin.
- Eğlenebilir, dalga geçebilir ama yerinde.

ÇINAR HAKKINDA BİLDİKLERİN:
- 21 yaşında, Konya'da yaşıyor
- Vali Necati Çetinkaya Ortaokulu'nda genel görevli
- YouTube kanalı VFXter — sinematik araba editleri, Shorts odaklı
- BMW M4/M5, Porsche, Nissan GTR, JDM kültürü sever
- CapCut Pro, Topaz Video AI kullanır
- Dark White adında 2D sinematik oyun geliştiriyor
- Matrix temalı sanal dünya projesi var
- Galatasaray taraftarı
- Marvel/Spider-Man sever
- Arkadaşları: Mert ve Hakan
- Roblox (Brookhaven, Blox Fruits), Minecraft Java
- 3 monitörlü gaming/editing setup hedefi var (100k TL bütçe)
- Python, Lua, Termux, GitHub Codespaces kullanır

GÖREV YÖNLENDIRME:
- Kod sorusu gelirse: [CODE] tag'i ile başla
- Arama/araştırma gerekirse: [SEARCH] tag'i ile başla  
- Hızlı cevap için: [FAST] tag'i ile başla
- Normal sohbet: tag yok

Her zaman Türkçe konuş. Çınar İngilizce yazmadıkça İngilizce konuşma."""

async def detect_intent(message: str) -> str:
    """Mesajın amacını tespit et, doğru modeli seç."""
    msg_lower = message.lower()
    
    code_keywords = ["kod", "script", "python", "lua", "hata", "error", "bug", "fix", "yaz", "fonksiyon", "class", "api"]
    search_keywords = ["ara", "bul", "nedir", "ne zaman", "kim", "haber", "güncel", "son"]
    
    if any(k in msg_lower for k in code_keywords):
        return "code"
    elif any(k in msg_lower for k in search_keywords):
        return "search"
    else:
        return "chat"

async def chat(session_id: str, user_message: str) -> dict:
    intent = await detect_intent(user_message)
    model = MODELS.get(intent, DEFAULT_MODEL)
    
    history = await get_history(session_id, limit=15)
    facts = await get_all_facts()
    
    system = ARTY_SYSTEM_PROMPT
    if facts:
        facts_str = "\n".join([f"- {k}: {v}" for k, v in facts.items()])
        system += f"\n\nHAFIZADAN NOTLAR:\n{facts_str}"
    
    messages = history + [{"role": "user", "content": user_message}]
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://artyai.local",
                "X-Title": "ArtyAI"
            },
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}] + messages,
                "max_tokens": 1024,
                "temperature": 0.85
            }
        )
        data = response.json()
    
    if "choices" not in data:
        error_msg = data.get("error", {}).get("message", str(data))
        raise Exception(f"OpenRouter error: {error_msg}")
    
    assistant_message = data["choices"][0]["message"]["content"]
    
    await save_message(session_id, "user", user_message)
    await save_message(session_id, "assistant", assistant_message, model)
    
    return {
        "message": assistant_message,
        "model": model,
        "intent": intent
    }
