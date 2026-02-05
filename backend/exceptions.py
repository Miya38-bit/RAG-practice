class RAGException(Exception):
    def __init__(self,message:str, details:dict | None = None):
        self.message = message
        self.details = details
        super().__init__(message)


class EmbeddingError(RAGException):
    pass


class SearchError(RAGException):
    pass


class LLMError(RAGException):
    pass
