import requests

# Ollama API yapılandırması
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3"

def _call_ollama(prompt):
    """Ollama API'sine istek gönderen yardımcı fonksiyon."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status() # Hata varsa istisna fırlatır
    data = response.json()
    return data.get("response", "")

def generate_summary(text):
    """Verilen metni Türkçe olarak özetler."""
    prompt = f"""
Aşağıdaki metni kısa, açık ve anlaşılır şekilde Türkçe özetle.

Metin:
{text}

Özet:
"""

    try:
        summary = _call_ollama(prompt).strip()
        return summary or "Özet üretilemedi."
    except Exception as e:
        return f"Özet oluşturulurken hata oluştu: {str(e)}"

def generate_tags(text):
    """Metinle ilgili 4-6 adet Türkçe etiket (tag) üretir."""
    prompt = f"""
Aşağıdaki metin için en uygun 4 ila 6 kısa etiketi Türkçe olarak üret.

Kurallar:
- Sadece etiketleri ver.
- Açıklama yazma.
- Etiketleri virgülle ayır.
- Etiketler kısa ve anlaşılır olsun.
- Küçük harf kullan.

Metin:
{text}

Etiketler:
"""

    try:
        tags = _call_ollama(prompt).strip()
        return tags or "Etiket üretilemedi."
    except Exception as e:
        return f"Etiket oluşturulurken hata oluştu: {str(e)}"
