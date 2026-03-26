from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.media_routes import router as media_router

app = FastAPI(title="AWS Manager")

# Configuração de CORS (Permite que o navegador do Front-End se comunique com a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, limite isso para a(s) URL(s) do seu Front-End
    allow_credentials=True,
    allow_methods=["*"],  # Permite opções como GET, POST e o problema atual: OPTIONS
    allow_headers=["*"],
)

# Registro das rotas de forma limpa
app.include_router(media_router, prefix="/storage")

@app.get("/health")
def health_check():
    return {"status": "online"}