# Lei Esquematizada Backend

API para processar leis em PDF e gerar esquematização com IA via OpenRouter.

## Instalação

```bash
git clone <repo-url>
cd lei-esquematizada-backend
cp .env.example .env
pip install -r requirements.txt
```

## Configuração

Edite o arquivo `.env` e defina sua chave da OpenRouter:

```
OPENROUTER_API_KEY=your_openrouter_key_here
```

## Execução local

```bash
uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t lei-esquematizada-backend .
docker run -p 8080:8080 --env-file .env lei-esquematizada-backend
```

## Endpoints

- **POST /processar/**  
  - Upload: PDF  
  - Retorno: JSON com estrutura da lei e esquematização.
