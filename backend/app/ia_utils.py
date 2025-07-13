import os
import httpx

OPENROUTER_API_KEY = os.getenv("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")  # Coloque sua key no ambiente

async def call_openrouter(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",  # ou outro modelo disponível para você
        "messages": messages,
        "temperature": 0.2
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
