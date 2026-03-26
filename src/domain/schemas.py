from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

####### SCHEMAS #######
class file_schema(BaseModel):
    """Representa um arquivo real no bucket (jpg, png, pdf, tiff, etc)"""
    name: str
    full_key: str
    size_bytes: int
    last_modified: datetime
    url: Optional[str] = None # Para download direto ou preview

class folder_schema(BaseModel):
    """Representa um prefixo (pasta) no bucket"""
    name: str
    full_path: str
    
####### REQUESTS #######
class list_request(BaseModel):
    """Requisição para listar objetos no bucket"""
    path: str
    delimiter: str
    storage_type: str

class create_folder_request(BaseModel):
    """Requisição para criar uma pasta"""
    path: str
    storage_type: str

class upload_request(BaseModel):
    """Requisição para upload de arquivo"""
    local_path: str
    remote_path: str
    storage_type: str

class delete_request(BaseModel):
    """Requisição para deletar um arquivo"""
    path: str
    storage_type: str

####### RESPONSES #######
class list_response(BaseModel):
    """O retorno completo para o Front-end ao listar um diretório"""
    current_path: str
    folders: List[folder_schema]
    files: List[file_schema]

class upload_response(BaseModel):
    """Resposta após um upload bem-sucedido"""
    message: str
    file_key: str
    url: str

class delete_response(BaseModel):
    """Resposta após uma deleção bem-sucedida"""
    message: str
    file_key: str
