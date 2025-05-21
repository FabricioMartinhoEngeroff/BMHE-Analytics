from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ResourceConflictException(HTTPException):
    def __init__(self, detail: str = "Recurso já existe ou está em conflito"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class MissingFieldException(HTTPException):
    def __init__(self, detail: str = "Campo obrigatório ausente"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
