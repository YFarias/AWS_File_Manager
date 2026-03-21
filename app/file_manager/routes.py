from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import AuthenticatedUser, get_current_user
from app.db.session import get_db
from app.file_manager.schemas import DownloadURLResponse, FileResponse
from app.file_manager.service import FileService
from app.infrastructure.s3_client import S3Client, get_s3_client

router = APIRouter(tags=["file_manager"])


def get_file_service(
    db: AsyncSession = Depends(get_db),
    s3_client: S3Client = Depends(get_s3_client),
) -> FileService:
    return FileService(db=db, s3_client=s3_client)


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
) -> FileResponse:
    return await service.upload_file(file=file, user_id=current_user.user_id)


@router.get("/download/{id}", response_model=DownloadURLResponse)
async def get_download_url(
    id: int,
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: FileService = Depends(get_file_service),
) -> DownloadURLResponse:
    return await service.get_download_url(file_id=id, user_id=current_user.user_id)
