class BaseAppException(Exception):
    """Classe base para exceções da aplicação."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
