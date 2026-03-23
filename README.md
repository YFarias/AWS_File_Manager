# AWS File Manager

Microservico FastAPI para listar arquivos e pastas no AWS S3.

## Requisitos

- Python 3.11+
- Credenciais AWS com acesso ao bucket S3

## Configuracao de ambiente

O projeto le variaveis do arquivo `.env` na raiz.

Variaveis usadas:

- `AWS_ACCESS_KEY_ID` (ou `VITE_AWS_ACCESS_KEY_ID`)
- `AWS_SECRET_ACCESS_KEY` (ou `VITE_AWS_SECRET_ACCESS_KEY`)
- `AWS_REGION` (ou `VITE_AWS_REGION`)
- `AWS_S3_BUCKET` (ou `VITE_AWS_BUCKET_A` / `VITE_AWS_BUCKET_B`)
- `S3_PRESIGNED_URL_EXPIRES_IN` (opcional, padrao `900`)

## Como iniciar o projeto

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

## Rotas disponiveis

- `GET /health`
- `POST /storage/list`
- `POST /storage/create-folder`
- `POST /storage/upload`

## Teste rapido

Com o servidor rodando em `http://127.0.0.1:8000`:

```bash
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/storage/list" -X POST -H "Content-Type: application/json" -d "{\"path\":\"\",\"storage_type\":\"A\"}"
```

Documentacao interativa:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
