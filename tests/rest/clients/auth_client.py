from tests.rest.core.http_client import HttpClient
from tests.rest.models.model import RegisterRequest, UserResponseDto, AuthRequest, AuthFullResponse


class AuthAPI(HttpClient):
    def register(self, req: RegisterRequest) -> UserResponseDto:
        return self._send_request(
            method="POST",
            path="/api/auth/register",
            step_title=f"Регистрация пользователя: {req.username}",
            json=req,
            expected_model=UserResponseDto
        )

    def login(self, req: AuthRequest) -> AuthFullResponse:
        return self._send_request(
            method="POST",
            path="/api/auth/login",
            step_title=f"Авторизация пользователя: {req.username}",
            json=req,
            expected_model=AuthFullResponse
        )