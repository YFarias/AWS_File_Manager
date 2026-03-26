from src.application.media_service import MediaService
from src.infrastructure.s3_client import S3Client, get_s3_client
import fastapi
import tkinter as tk
from tkinter import filedialog
import os
from pathlib import Path

router = fastapi.APIRouter()

from src.domain.schemas import (
    list_request, 
    create_folder_request, 
    upload_request, 
    delete_request,
    rename_request
)

### MAIN METHODS ### 
# aws s3 ls s3://idecanstorage/idecan-app-files/File/img_pref_jp/ 
@router.post("/list")     
async def list_path(request: list_request, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).list_folder(request)  

#aws s3api put-object --bucket idecanstorage --key "idecan-app-files/File/img_pref_jp/..etc"
@router.post("/create-folder")
async def create_folder(request: create_folder_request, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).create_folder(request)

from typing import List

# Arquivo enviado pelo front-end (multipart/form-data)
@router.post("/upload")
async def upload_files_from_web(
    storage_type: str = fastapi.Form(...),
    remote_path: str = fastapi.Form(""),
    files: List[fastapi.UploadFile] = fastapi.File(...),
    s3_client: S3Client = fastapi.Depends(get_s3_client)
):
    return await MediaService(s3_client).upload_web_files(storage_type, remote_path, files)

#aws s3 rm s3://meu-bucket/remote-folder/file.txt
@router.post("/delete")
async def delete(request: delete_request, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).delete(request)


@router.put("/rename")
async def rename(request: rename_request, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).rename(request)

### EXTRA METHOD ###
#get folder path
@router.get("/select-folder")
async def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = filedialog.askdirectory()

    root.destroy()

    if not path:
        return {"error": "Nenhuma pasta selecionada"}

    # Adicionado .tiff e busca recursiva se desejar
    extensoes_alvo = {'.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.tif', '.tiff'}
    
    arquivos_encontrados = []
    
    # Use rglob("*") para buscar em subpastas ou glob("*") para apenas a pasta atual
    for item in Path(path).glob("*"): 
        if item.is_file() and item.suffix.lower() in extensoes_alvo:
            arquivos_encontrados.append({
                "nome": item.name,
                "extensao": item.suffix,
                "caminho_completo": str(item.absolute())
            })

    return {
        "pasta_selecionada": path,
        "total_arquivos": len(arquivos_encontrados),
        "arquivos": arquivos_encontrados
    }



