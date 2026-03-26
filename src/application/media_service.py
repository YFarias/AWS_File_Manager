from typing import List
import os
from pathlib import Path
from fastapi import UploadFile
from src.infrastructure.s3_client import S3Client
from src.domain.schemas import (
    list_request, 
    file_schema, 
    folder_schema, 
    list_response, 
    create_folder_request, 
    delete_request
)
from datetime import datetime


class MediaService:
    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client

    # aws s3 ls
    async def list_folder(self, request: list_request) -> list_response:
        bucket = self.s3_client.get_bucket(request.storage_type)
        normalized_path = request.path.strip("/")
        if normalized_path:
            normalized_path += "/"
        
        response = self.s3_client.list_objects(
            Bucket=bucket,
            Prefix=normalized_path,
            Delimiter="/"
        )

        files: List[file_schema] = []
        if "Contents" in response:
            for obj in response["Contents"]:
                if obj["Key"] == normalized_path:
                    continue
                
                url = self.s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket, "Key": obj["Key"]},
                    ExpiresIn=3600
                )

                files.append(file_schema(
                    name=obj["Key"].replace(normalized_path, ""),
                    full_key=obj["Key"],
                    size_bytes=obj["Size"],
                    last_modified=obj["LastModified"],
                    url=url
                ))

        # 4. Processa os Delimitadores (Pastas)
        folders: List[folder_schema] = []
        if "CommonPrefixes" in response:
            for prefix in response["CommonPrefixes"]:
                folder_key = prefix["Prefix"]
                folders.append(folder_schema(
                    name=folder_key.replace(normalized_path, ""),
                    full_path=folder_key
                ))

        return list_response(
            current_path=normalized_path,
            folders=folders,
            files=files
        )
    
    async def create_folder(self, request: create_folder_request) -> folder_schema:
        bucket = self.s3_client.get_bucket(request.storage_type)
        normalized_path = request.path.strip("/")
        if normalized_path:
            normalized_path += "/"
        
        self.s3_client.put_object(
            Bucket=bucket,
            Key=normalized_path
        )
        
        return folder_schema(
            name=normalized_path,
            full_path=normalized_path
        )
    
    async def upload_web_files(self, storage_type: str, remote_path: str, files: List[UploadFile]) -> List[file_schema]:
        """
        Recebe arquivos do front-end e os envia em memória para o S3.
        """
        bucket = self.s3_client.get_bucket(storage_type)
        uploaded_files = []
        
        remote_path = remote_path.strip("/")
        if remote_path:
            remote_path += "/"

        for file in files:
            # Pega o caminho/nome do arquivo
            filename = file.filename or f"unnamed_{datetime.now().timestamp()}"
            s3_key = os.path.join(remote_path, filename).replace("\\", "/")
            
            # Descobrindo o tamanho do arquivo em memória (necessário para o file_schema)
            file.file.seek(0, 2)
            file_size = file.file.tell()
            file.file.seek(0)
            
            # Enviamos o arquivo em memória para o S3Client
            success = self.s3_client.upload_fileobj(bucket, file.file, s3_key)
            
            if success:
                uploaded_files.append(file_schema(
                    name=os.path.basename(filename),
                    full_key=s3_key,
                    size_bytes=file_size,
                    last_modified=datetime.now(),
                    url=self.s3_client.generate_presigned_url(
                        "get_object",
                        Params={"Bucket": bucket, "Key": s3_key},
                        ExpiresIn=3600
                    )
                ))

        return uploaded_files

    async def delete(self, request: delete_request) -> bool:
        try:
            bucket = self.s3_client.get_bucket(request.storage_type)
            self.s3_client.delete(bucket, request.path)
            return True
        except Exception as e:
            raise Exception(f"Erro ao deletar arquivo: {e}")