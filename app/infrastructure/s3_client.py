from __future__ import annotations

from functools import lru_cache
from typing import BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import Settings, get_settings
from app.file_manager.exceptions import S3DeleteError, S3DownloadError, S3UploadError


class S3Client:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._bucket = self._settings.aws_s3_bucket

        if not self._bucket:
            raise ValueError("AWS_S3_BUCKET must be configured.")

        self._client = boto3.client(
            "s3",
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
            region_name=self._settings.aws_region,
        )

    def upload(self, file_obj: BinaryIO, key: str, content_type: str | None = None) -> str:
        upload_args: dict[str, str] = {}
        if content_type:
            upload_args["ContentType"] = content_type

        try:
            file_obj.seek(0)
            if upload_args:
                self._client.upload_fileobj(file_obj, self._bucket, key, ExtraArgs=upload_args)
            else:
                self._client.upload_fileobj(file_obj, self._bucket, key)
        except (ClientError, BotoCoreError, OSError) as exc:
            raise S3UploadError() from exc

        return key

    def download(self, key: str, expires_in: int = 900) -> str:
        try:
            return self._client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        except (ClientError, BotoCoreError) as exc:
            raise S3DownloadError() from exc

    def delete(self, key: str) -> None:
        try:
            self._client.delete_object(Bucket=self._bucket, Key=key)
        except (ClientError, BotoCoreError) as exc:
            raise S3DeleteError() from exc


@lru_cache(maxsize=1)
def get_s3_client() -> S3Client:
    return S3Client()
