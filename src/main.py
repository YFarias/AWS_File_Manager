from fastapi import FastAPI
from src.api.media_routes import router as media_router

app = FastAPI(title="AWS Manager")

# Registro das rotas de forma limpa
app.include_router(media_router, prefix="/storage")

@app.get("/health")
def health_check():
    return {"status": "online"}