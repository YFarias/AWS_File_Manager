from src.domain.schemas import DeleteResponse, UploadResponse
from src.application.media_service import MediaService
from src.infrastructure.s3_client import S3Client, get_s3_client
import fastapi

router = fastapi.APIRouter()

from src.domain.schemas import S3ListRequest, S3CreateFolderRequest, UploadRequest, delete_request

# aws s3 ls 
@router.post("/list")     
async def list_path(request: S3ListRequest, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).list_folder(request)  

#aws s3api put-object --bucket idecanstorage --key "idecan-app-files/File/img_pref_jp/..etc"
@router.post("/create-folder")
async def create_folder(request: S3CreateFolderRequest, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).create_folder(request)

#aws s3 sync ./local-folder s3://meu-bucket/remote-folder
@router.post("/upload")
async def upload(request: UploadRequest, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).upload(request)

@router.post("/delete")
async def delete(request: delete_request, s3_client: S3Client = fastapi.Depends(get_s3_client)):
    return await MediaService(s3_client).delete(request)