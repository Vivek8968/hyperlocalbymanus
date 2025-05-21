from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, List, Union


class AppException(HTTPException):
    """
    Base exception class for application-specific exceptions
    """
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        code: str = "error"
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code


class ResourceNotFoundException(AppException):
    """
    Exception raised when a requested resource is not found
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code="resource_not_found"
        )


class UnauthorizedException(AppException):
    """
    Exception raised when a user is not authorized to access a resource
    """
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code="unauthorized",
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(AppException):
    """
    Exception raised when a user is forbidden from accessing a resource
    """
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code="forbidden"
        )


class ValidationException(AppException):
    """
    Exception raised when request validation fails
    """
    def __init__(self, detail: Union[str, List[Dict[str, Any]]] = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code="validation_error"
        )


class DatabaseException(AppException):
    """
    Exception raised when a database operation fails
    """
    def __init__(self, detail: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            code="database_error"
        )


class ExternalServiceException(AppException):
    """
    Exception raised when an external service call fails
    """
    def __init__(self, detail: str = "External service error"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            code="external_service_error"
        )


async def exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Global exception handler for AppException
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.detail,
            "path": request.url.path
        }
    )
