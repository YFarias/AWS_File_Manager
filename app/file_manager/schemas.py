from pydantic import BaseModel, ConfigDict, Field


class FileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    user_id: str = Field(min_length=1, max_length=255)


class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    s3_key: str
    size: int
    user_id: str


class DownloadURLResponse(BaseModel):
    file_id: int
    download_url: str
