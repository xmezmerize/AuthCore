class DatabaseError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(DatabaseError):
    def __init__(self, entity: str, identifier: str):
        super().__init__(f"{entity} com identificador {identifier} não encontrado.", status_code=404)

class ConflictError(DatabaseError):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)
