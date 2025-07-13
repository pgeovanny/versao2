from app.ia_utils import call_openrouter

async def organizar_ia_real(sections):
    prompt = (
        "Você é um especialista em legislação. Sua tarefa é analisar o texto de cada artigo da lei e organizar a estrutura de forma lógica, clara, e com visual facilitador para estudo. "
        "Agrupe por tópicos, separe os artigos, destaque prazos, regras absolutas (em negrito), palavras negativas (em vermelho), faça tabelas para composições e prazos, sempre que houver. "
        "Seu objetivo é facilitar a compreensão para concursos, sempre mantendo a literalidade do texto onde importante. Nunca resuma demais, apenas organize e realce o que for fundamental."
    )
    results = []
    for sec in sections:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Artigo: {sec.content}"}
        ]
        content = await call_openrouter(messages)
        results.append({"title": sec.title, "content": content})
    return results

async def esquematizar_ia_real(sections):
    prompt = (
        "Você é um especialista em esquematização de leis. Para cada artigo, crie esquemas visuais, quadros, tabelas comparativas, destaque prazos, grife palavras negativas de vermelho, regras absolutas em negrito e crie fluxogramas ou quadros nos artigos mais complexos."
        "Para todos os artigos, repita a literalidade destacando o mais importante. A apresentação deve ser clara, bonita, fácil para estudo e revisão. Use sempre a estrutura markdown, HTML básico, emojis, quadros e tabelas quando útil."
    )
    results = []
    for sec in sections:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Artigo: {sec.content}"}
        ]
        content = await call_openrouter(messages)
        results.append({"title": sec.title, "schematization": content})
    return results
