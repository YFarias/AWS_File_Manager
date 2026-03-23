from __future__ import annotations

from functools import lru_cache
from typing import BinaryIO
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.core.config import Settings, get_settings
from src.domain.exceptions import S3ListError, S3UploadError, S3DeleteError, S3DownloadError    


class S3Client:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

        self._client = boto3.client(
            "s3",
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
            region_name=self._settings.aws_region,
        )

    def get_bucket(self, storage_type: str) -> str:
        if storage_type.upper() in ["A", "IDECAN", "IDECANSTORAGE"]:
            return self._settings.aws_bucket_a
        elif storage_type.upper() in ["B", "IDIB", "IDIBSTORAGE"]:
            return self._settings.aws_bucket_b
        elif storage_type in [self._settings.aws_bucket_a, self._settings.aws_bucket_b]:
            return storage_type
            
        if self._settings.aws_bucket_a:
            return self._settings.aws_bucket_a
        raise ValueError(f"Bucket não configurado para o tipo: {storage_type}")    #aws s3 ls "s3://idecanstorage/idecan-app-files/File/img_pref_jp/StorageTest/"
    def list_objects(self, Bucket: str, Prefix: str, Delimiter: str) -> dict:
        """Lista objetos em um bucket com prefixo e delimitador."""
        try:
            return self._client.list_objects(Bucket=Bucket, Prefix=Prefix, Delimiter=Delimiter)
        except (ClientError, BotoCoreError) as exc:
            raise S3ListError("Erro ao listar objetos no bucket.", exc) from exc
    
    #aws s3 mb s3://idecanstorage
    def put_object(self, Bucket: str, Key: str) -> dict:
        """Cria uma pasta no bucket."""
        try:
            return self._client.put_object(Bucket=Bucket, Key=Key)
        except (ClientError, BotoCoreError) as exc:
            raise S3UploadError("Erro ao criar pasta.", exc) from exc
    
    def generate_presigned_url(self, ClientMethod: str, Params: dict, ExpiresIn: int) -> str:
        """Gera uma URL pré-assinada para um objeto."""
        try:
            return self._client.generate_presigned_url(ClientMethod, Params, ExpiresIn)
        except (ClientError, BotoCoreError) as exc:
            raise S3DownloadError("Erro ao gerar URL pré-assinada.", exc) from exc
    
    #aws s3 sync "./local-folder" "s3://meu-bucket/remote-folder"
    def sync_file(self, bucket: str, local_path: str, remote_key: str) -> bool:
        
        try:
            # 1. Tenta pegar os metadados do arquivo no S3
            head = self._client.head_object(Bucket=bucket, Key=remote_key)
            s3_size = head['ContentLength']
            
            # 2. Compara com o arquivo local
            local_size = os.path.getsize(local_path)
            
            if s3_size == local_size:
                print(f"Arquivo {remote_key} já está atualizado. Pulando...")
                return False
                
        except ClientError:
            # Se cair aqui, é porque o arquivo não existe no S3 (404)
            pass

        # 3. Se não existe ou o tamanho é diferente, faz o upload
        self._client.upload_file(local_path, bucket, remote_key)
        print(f"Subindo: {local_path} -> {remote_key}")
        return True

    def download(self, bucket: str, key: str, expires_in: int = 900) -> str:
        try:
            return self._client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        except (ClientError, BotoCoreError) as exc:
            raise S3DownloadError("Erro ao gerar URL pré-assinada.", exc) from exc

    #aws s3 rm "s3://idecanstorage/idecan-app-files/File/img_pref_jp/StorageTest/2204392.jpeg"
    def delete(self, bucket: str, key: str) -> None:
        try:
            self._client.delete_object(Bucket=bucket, Key=key)
        except (ClientError, BotoCoreError) as exc:
            raise S3DeleteError("Erro ao deletar objeto.", exc) from exc

@lru_cache(maxsize=1)
def get_s3_client() -> S3Client:
    return S3Client()
