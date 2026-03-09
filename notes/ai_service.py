import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3"


def _call_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")


def generate_summary(text):
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