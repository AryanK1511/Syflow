from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.constants import PUBLIC_ENDPOINTS
from backend.app.response import error_response
from backend.app.services.auth.jwt_validation import VerifyToken


class TokenVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_ENDPOINTS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                error_response(
                    message="Missing Authorization header",
                    error={"message": "No 'Authorization' header found"},
                ).model_dump(),
                status_code=401,
            )

        if not auth_header.lower().startswith("bearer "):
            return JSONResponse(
                error_response(
                    message="Invalid token format",
                    error={"message": "Expected 'Bearer <token>' format"},
                ).model_dump(),
                status_code=401,
            )

        token = auth_header.split(" ")[1]

        verify = VerifyToken(token).verify()
        if verify.get("status", "error") == "error":
            return JSONResponse(
                error_response(
                    message="Token verification failed", error=verify
                ).model_dump(),
                status_code=400,
            )

        response = await call_next(request)
        return response
