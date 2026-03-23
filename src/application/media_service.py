from typing import List
import os
from pathlib import Path
from src.infrastructure.s3_client import S3Client
from src.domain.schemas import (
    list_request, 
    file_schema, 
    folder_schema, 
    list_response, 
    create_folder_request, 
    upload_request, 
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
    
    # aws s3 sync "./local-folder" "s3://meu-bucket/remote-folder"
    async def upload(self, request: upload_request) -> List[file_schema]:
        """
        Replica o 'aws s3 sync local_path s3://bucket/prefix'
        """
        bucket = self.s3_client.get_bucket(request.storage_type)
        uploaded_files = []
        local_path = Path(request.local_path)
        remote_path = request.remote_path.strip("/")
        if remote_path:
            remote_path += "/"

        if not local_path.exists():
            raise ValueError(f"O caminho local {request.local_path} não existe.")

        for root, dirs, files in os.walk(request.local_path):
            for file in files:
                local_file_path = Path(root) / file
                
                relative_path = local_file_path.relative_to(local_path)
                s3_key = os.path.join(remote_path, str(relative_path)).replace("\\", "/")

                uploaded = self.s3_client.sync_file(bucket, str(local_file_path), s3_key)
                
                if uploaded:
                    uploaded_files.append(file_schema(
                        name=file,
                        full_key=s3_key,
                        size_bytes=os.path.getsize(local_file_path),
                        last_modified=datetime.fromtimestamp(os.path.getmtime(local_file_path)),
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
            self.s3_client.delete(bucket, request.file_key)
            return True
        except Exception as e:
            raise Exception(f"Erro ao deletar arquivo: {e}")