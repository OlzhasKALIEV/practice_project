from typing import List

import requests

from tests.rest.core.http_client import HttpClient
from tests.rest.models.model import IngredientResponseDto, IngredientRequestDto


class IngredientsAPI(HttpClient):
    """API клиент для работы с ингредиентами"""

    def get_all(self) -> List[IngredientResponseDto]:
        """Получает список всех ингредиентов"""
        return self._send_request(
            method="GET",
            path="/api/ingredients",
            step_title="Получение всех ингредиентов",
            expected_model=List[IngredientResponseDto]
        )

    def get_available(self) -> List[IngredientResponseDto]:
        """Получает только доступные ингредиенты (quantity > 0)"""
        return self._send_request(
            method="GET",
            path="/api/ingredients/available",
            step_title="Получение доступных ингредиентов",
            expected_model=List[IngredientResponseDto]
        )

    def get_by_id(self, ingredient_id: int) -> IngredientResponseDto:
        """Получает конкретный ингредиент по ID"""
        return self._send_request(
            method="GET",
            path=f"/api/ingredients/{ingredient_id}",
            step_title=f"Получение ингредиента по ID: {ingredient_id}",
            expected_model=IngredientResponseDto
        )

    def create(self, dto: IngredientRequestDto) -> IngredientResponseDto:
        """Создает новый ингредиент (только для SELLER/ADMIN)"""
        return self._send_request(
            method="POST",
            path="/api/ingredients",
            step_title=f"Создание нового ингредиента: {dto.name}",
            json=dto,
            expected_model=IngredientResponseDto
        )

    def update(self, ingredient_id: int, dto: IngredientRequestDto) -> IngredientResponseDto:
        """Обновляет существующий ингредиент"""
        return self._send_request(
            method="PUT",
            path=f"/api/ingredients/{ingredient_id}",
            step_title=f"Обновление ингредиента по ID: {ingredient_id}",
            json=dto,
            expected_model=IngredientResponseDto
        )

    def delete(self, ingredient_id: int) -> requests.Response:
        """Удаляет ингредиент"""
        return self._send_request(
            method="DELETE",
            path=f"/api/ingredients/{ingredient_id}",
            step_title=f"Удаление ингредиента по ID: {ingredient_id}"
            # Не указываем expected_model, вернется requests.Response
        )