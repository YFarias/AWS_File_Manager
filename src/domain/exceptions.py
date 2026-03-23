from botocore.exceptions import ClientError, BotoCoreError



##ListError, UploadError, DeleteError, DownloadError###    
class S3ListError(Exception):
    """Erro ao listar objetos no bucket."""
    def __init__(self, message: str, error: ClientError | BotoCoreError):
        super().__init__(message)
        self.error = error
    pass

class S3UploadError(Exception):
    """Erro ao fazer upload de um objeto."""
    def __init__(self, message: str, error: ClientError | BotoCoreError | OSError):
        super().__init__(message)
        self.error = error
    pass

class S3DeleteError(Exception):
    """Erro ao deletar um objeto."""
    def __init__(self, message: str, error: ClientError | BotoCoreError):
        super().__init__(message)
        self.error = error
    pass

class S3DownloadError(Exception):
    """Erro ao fazer download de um objeto."""
    def __init__(self, message: str, error: ClientError | BotoCoreError):
        super().__init__(message)
        self.error = error
    pass

