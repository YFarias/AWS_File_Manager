from app.core.exceptions import BaseAppException


class S3UploadError(BaseAppException):
    def __init__(self, message: str = "Failed to upload file to S3.") -> None:
        super().__init__(message=message, code="S3_UPLOAD_ERROR", status_code=502)


class S3DownloadError(BaseAppException):
    def __init__(self, message: str = "Failed to generate S3 download URL.") -> None:
        super().__init__(message=message, code="S3_DOWNLOAD_ERROR", status_code=502)


class S3DeleteError(BaseAppException):
    def __init__(self, message: str = "Failed to delete file from S3.") -> None:
        super().__init__(message=message, code="S3_DELETE_ERROR", status_code=502)


class FileTooLargeError(BaseAppException):
    def __init__(self, max_size_bytes: int) -> None:
        super().__init__(
            message=f"The file exceeds the maximum allowed size of {max_size_bytes} bytes.",
            code="FILE_TOO_LARGE",
            status_code=413,
        )


class FileRecordNotFoundError(BaseAppException):
    def __init__(self, file_id: int) -> None:
        super().__init__(
            message=f"File with id {file_id} was not found.",
            code="FILE_NOT_FOUND",
            status_code=404,
        )
