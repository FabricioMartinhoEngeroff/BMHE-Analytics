from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ResourceConflictException(HTTPException):
    def __init__(self, detail: str = "Recurso já existe"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
