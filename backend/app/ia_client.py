import httpx
from typing import List, Dict
from .settings import settings

class IAClient:
    def __init__(self):
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json"
        }

    async def sumarize(self, structure: List) -> List[Dict]:
        results = []
        for section in structure:
            data = section.dict() if hasattr(section, "dict") else section
            prompt = (
                f"Você é um especialista em organização, didática e legislação. Sua missão é analisar e organizar o texto a seguir "
                f"para criar uma versão mais lógica, visual e didática, mantendo a fidelidade ao conteúdo. "
                f"Organize em tópicos, destaques, separando ideias principais e secundárias, já destacando trechos essenciais, "
                f"como prazos, composições, obrigações, conceitos, exceções e palavras negativas (destaque-as visualmente). "
                f"Facilite ao máximo a leitura para que a próxima etapa de esquematização seja mais eficiente e visual.\n\n"
                f"Título: {data['title']}\n"
                f"Conteúdo:\n{data['content']}\n\n"
                f"Reestruture, destaque e organize. Não crie quadros ou tabelas ainda, mas utilize tópicos e marcações claras. "
                f"Retorne sempre todo o conteúdo reorganizado, nunca omita artigos."
            )
            generated = await self._call_ia(prompt)
            results.append({
                "title": data["title"],
                "schematization": generated
            })
        return results

    async def schematize(self, structure: List) -> List[Dict]:
        results = []
        for section in structure:
            data = section.dict() if hasattr(section, "dict") else section
            prompt = (
                f"Você é um especialista em esquematização legislativa, didática avançada e técnicas de memorização. "
                f"Esquematize TODO o conteúdo a seguir, criando para cada artigo da legislação ao menos um destaque relevante. "
                f"Em artigos importantes, elabore quadros comparativos, tabelas, fluxogramas, mapas mentais, ou resumos visuais. "
                f"Sempre destaque prazos, composições, exceções, regras absolutas, conceitos essenciais, criando marcações visuais "
                f"(exemplo: palavras negativas em vermelho, prazos em negrito, pontos críticos em amarelo, conceitos em caixas etc). "
                f"NUNCA pule nenhum artigo. Para artigos simples, faça pelo menos um grifo inteligente; para artigos importantes, "
                f"aprofundar com recursos visuais facilitadores. O resultado deve ser o mais didático e visual possível, em Markdown.\n\n"
                f"Título: {data['title']}\n"
                f"Conteúdo:\n{data['content']}\n\n"
                f"Responda apenas com o esquema visual proposto para esse artigo."
            )
            generated = await self._call_ia(prompt)
            results.append({
                "title": data["title"],
                "schematization": generated
            })
        return results

    async def _call_ia(self, prompt: str) -> str:
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é um especialista em esquematização de leis brasileiras."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": settings.max_chunk_tokens,
            "temperature": 0.2
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.url, headers=self.headers, json=payload, timeout=60.0)
            if resp.status_code != 200:
                raise Exception(f"OpenRouter error {resp.status_code}: {resp.text}")
            data = resp.json()
            return data["choices"][0]["message"]["content"]
