from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.media_routes import router as media_router

app = FastAPI(title="AWS Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

app.include_router(media_router, prefix="/storage")

@app.get("/health")
def health_check():
    return {"status": "online"}