from fastapi import Request
from fastapi.responses import JSONResponse
from mcp_backend.app.exceptions.resource_exceptions import ResourceNotFoundException, ResourceConflictException
from mcp_backend.app.exceptions.security_exceptions import UnauthorizedException, ForbiddenException

def register_exception_handlers(app):
    @app.exception_handler(ResourceNotFoundException)
    async def not_found_handler(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(ResourceConflictException)
    async def conflict_handler(request: Request, exc: ResourceConflictException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
