from datetime import datetime
from typing import List

import pytest
from faker import Faker

from tests.db.db_executor import DbExecutor
from tests.db.ingredient_repo import IngredientRepository
from tests.db.orders_repo import OrderRepository
from tests.db.user_repo import UserRepository
from tests.helpers.user_builder import UserBuilder
from tests.rest.clients.auth_client import AuthAPI
from tests.rest.models.model import IngredientRequestDto


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8080"

@pytest.fixture(scope="session")
def professional_db_executor():
    return DbExecutor()

@pytest.fixture
def faker_instance():
    return Faker()

@pytest.fixture(scope="session")
def user_repository(professional_db_executor):
    return UserRepository(professional_db_executor)

@pytest.fixture(scope="session")
def ingredient_repository(professional_db_executor):
    return IngredientRepository(professional_db_executor)

@pytest.fixture(scope="session")
def order_repository(professional_db_executor):
    return OrderRepository(professional_db_executor)

@pytest.fixture(scope="session")
def auth_api_client(base_url):
    return AuthAPI(base_url)

@pytest.fixture
def user_builder(auth_api_client, user_repository, base_url) -> UserBuilder:
    """Эта фикстура теперь использует реальный UserRepository для обновления ролей."""
    return UserBuilder(auth_api_client, user_repository, base_url)

@pytest.fixture
def managed_ingredients(user_builder, faker_instance):
    """
    Фикстура-фабрика для создания и автоматической очистки ингредиентов.

    Возвращает функцию, которая:
    1. Создает указанное количество ингредиентов
    2. Запоминает их ID для последующей очистки
    3. После теста автоматически удаляет созданные ингредиенты

    Использование:
        ingredient_ids = managed_ingredients(count=3, quantity=5)
        # Создаст 3 ингредиента по 5 штук каждый
    """

    # Создаем пользователя с правами продавца для управления ингредиентами
    # Только SELLER и ADMIN могут создавать/удалять ингредиенты
    creator = user_builder.create_user(role="SELLER")
    ingredients_api = creator.clients.ingredients

    # Список для отслеживания созданных ингредиентов
    created_ids = []

    def _create(count: int = 1, quantity: int = 10) -> List[int]:
        """
        Внутренняя функция для создания ингредиентов.

        Args:
            count: Сколько ингредиентов создать
            quantity: Количество каждого ингредиента

        Returns:
            List[int]: Список ID созданных ингредиентов
        """
        nonlocal created_ids  # Используем переменную из внешней области
        ids = []

        # Создаем указанное количество ингредиентов
        for _ in range(count):
            # Генерируем уникальное имя ингредиента
            payload = IngredientRequestDto(
                name=f"Ингредиент-{faker_instance.unique.word()}-{datetime.now().microsecond}",
                quantity=quantity
            )

            # Создаем ингредиент через API
            response = ingredients_api.create(payload)
            ids.append(response.id)

        # Запоминаем ID для последующей очистки
        created_ids.extend(ids)
        return ids

    # Возвращаем функцию-фабрику
    yield _create

    # === CLEANUP (выполняется после теста) ===
    # Если ничего не создавали, очищать нечего
    if not created_ids:
        return