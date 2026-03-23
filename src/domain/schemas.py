from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

####### SCHEMAS #######
class S3FileSchema(BaseModel):
    """Representa um arquivo real no bucket (jpg, png, pdf, tiff, etc)"""
    name: str
    full_key: str
    size_bytes: int
    last_modified: datetime
    url: Optional[str] = None # Para download direto ou preview

class S3FolderSchema(BaseModel):
    """Representa um prefixo (pasta) no bucket"""
    name: str
    full_path: str
    
####### REQUESTS #######
class S3ListRequest(BaseModel):
    """Requisição para listar objetos no bucket"""
    path: str
    delimiter: str
    storage_type: str

class S3CreateFolderRequest(BaseModel):
    """Requisição para criar uma pasta"""
    path: str
    storage_type: str

class UploadRequest(BaseModel):
    """Requisição para upload de arquivo"""
    local_path: str
    remote_path: str
    storage_type: str

class delete_request(BaseModel):
    """Requisição para deletar um arquivo"""
    file_key: str
    storage_type: str

####### RESPONSES #######
class S3FolderContentResponse(BaseModel):
    """O retorno completo para o Front-end ao listar um diretório"""
    current_path: str
    folders: List[S3FolderSchema]
    files: List[S3FileSchema]

class UploadResponse(BaseModel):
    """Resposta após um upload bem-sucedido"""
    message: str
    file_key: str
    url: str

class DeleteResponse(BaseModel):
    """Resposta após uma deleção bem-sucedida"""
    message: str
    file_key: str
