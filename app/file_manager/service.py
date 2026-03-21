from __future__ import annotations

from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import BaseAppException
from app.file_manager.exceptions import FileRecordNotFoundError, FileTooLargeError
from app.file_manager.models import FileRecord
from app.file_manager.schemas import DownloadURLResponse, FileResponse
from app.infrastructure.s3_client import S3Client


class FileService:
    def __init__(
        self,
        db: AsyncSession,
        s3_client: S3Client,
        settings: Settings | None = None,
    ) -> None:
        self._db = db
        self._s3_client = s3_client
        self._settings = settings or get_settings()

    async def upload_file(self, file: UploadFile, user_id: str) -> FileResponse:
        file_name = (file.filename or "uploaded_file").strip()
        file_size = self._get_file_size(file)

        if file_size > self._settings.max_upload_size_bytes:
            raise FileTooLargeError(max_size_bytes=self._settings.max_upload_size_bytes)

        s3_key = self._build_s3_key(user_id=user_id, file_name=file_name)
        self._s3_client.upload(
            file_obj=file.file,
            key=s3_key,
            content_type=file.content_type,
        )

        file_record = FileRecord(
            name=file_name,
            s3_key=s3_key,
            size=file_size,
            user_id=user_id,
        )
        self._db.add(file_record)

        try:
            await self._db.commit()
            await self._db.refresh(file_record)
        except SQLAlchemyError as exc:
            await self._db.rollback()
            raise BaseAppException(
                message="Failed to persist file metadata.",
                code="DATABASE_ERROR",
                status_code=500,
            ) from exc

        return FileResponse.model_validate(file_record)

    async def get_download_url(self, file_id: int, user_id: str) -> DownloadURLResponse:
        query = select(FileRecord).where(
            FileRecord.id == file_id,
            FileRecord.user_id == user_id,
        )
        result = await self._db.execute(query)
        file_record = result.scalar_one_or_none()

        if file_record is None:
            raise FileRecordNotFoundError(file_id=file_id)

        download_url = self._s3_client.download(
            key=file_record.s3_key,
            expires_in=self._settings.s3_presigned_url_expires_in,
        )
        return DownloadURLResponse(file_id=file_record.id, download_url=download_url)

    @staticmethod
    def _get_file_size(file: UploadFile) -> int:
        current_position = file.file.tell()
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(current_position)
        return size

    @staticmethod
    def _build_s3_key(user_id: str, file_name: str) -> str:
        safe_user = user_id.strip().replace(" ", "_")
        safe_name = file_name.replace("/", "_").replace("\\", "_")
        return f"{safe_user}/{uuid4().hex}_{safe_name}"
