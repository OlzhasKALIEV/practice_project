from typing import List

import requests

from tests.rest.core.http_client import HttpClient
from tests.rest.models.models import UserResponseDto, UserRequestDto, PagedResponseUserResponseDto


class UsersAPI(HttpClient):
    """API клиент для работы с пользователями"""

    def create(self, dto: UserRequestDto) -> UserResponseDto:
        """Создает нового пользователя"""
        return self._send_request(
            method="POST",
            path="/api/users",
            step_title=f"Создание пользователя: {dto.username}",
            json=dto,
            expected_model=UserResponseDto
        )

    def get_all(self, params: dict = None) -> PagedResponseUserResponseDto:
        """Получает всех пользователей с пагинацией"""
        return self._send_request(
            method="GET",
            path="/api/users",
            step_title="Получение всех пользователей с пагинацией",
            params=params,
            expected_model=PagedResponseUserResponseDto
        )

    def get_all_no_pagination(self) -> List[UserResponseDto]:
        """Получает всех пользователей без пагинации"""
        return self._send_request(
            method="GET",
            path="/api/users/all",
            step_title="Получение всех пользователей без пагинации",
            expected_model=List[UserResponseDto]
        )

    def get_by_id(self, user_id: int) -> UserResponseDto:
        """Получает пользователя по ID"""
        return self._send_request(
            method="GET",
            path=f"/api/users/{user_id}",
            step_title=f"Получение пользователя по ID: {user_id}",
            expected_model=UserResponseDto
        )

    def update(self, user_id: int, dto: UserRequestDto) -> UserResponseDto:
        """Обновляет существующего пользователя"""
        return self._send_request(
            method="PUT",
            path=f"/api/users/{user_id}",
            step_title=f"Обновление пользователя ID: {user_id}",
            json=dto,
            expected_model=UserResponseDto
        )

    def delete(self, user_id: int) -> requests.Response:
        """Удаляет пользователя"""
        return self._send_request(
            method="DELETE",
            path=f"/api/users/{user_id}",
            step_title=f"Удаление пользователя по ID: {user_id}"
        )

    def export_users_with_orders(self, format_param: str) -> bytes:
        """Экспортирует пользователей с заказами"""
        response = self._send_request(
            method="GET",
            path="/api/users/export",
            step_title=f"Экспорт пользователей с заказами в формате: {format_param}",
            params={"format": format_param}
        )
        return response.content