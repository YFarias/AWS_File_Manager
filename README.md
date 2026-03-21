# AWS File Manager Microservice

Microservico em FastAPI (Python 3.11+) para upload/download de arquivos com metadados em banco e armazenamento no AWS S3.

## Estrutura

```text
AWS_File_Manager/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── file_manager/
│   │   ├── exceptions.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── infrastructure/
│   │   ├── redis_client.py
│   │   └── s3_client.py
│   └── main.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

## Endpoints

- `GET /health`
- `POST /upload`
- `GET /download/{id}`

## Executar localmente

```bash
python -m venv venv
# Windows: .\\venv\\Scripts\\Activate.ps1
# Linux/macOS: source venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Alembic

```bash
alembic revision --autogenerate -m "create files table"
alembic upgrade head
```
