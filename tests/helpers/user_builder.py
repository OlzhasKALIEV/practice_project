from datetime import datetime
import allure
from faker import Faker
from tests.db.user_repo import UserRepository
from tests.helpers.client_factory import ClientFactory
from tests.rest.clients.auth_client import AuthAPI
from tests.rest.models.models import UserResponseDto, RegisterRequest, AuthRequest


class User:
    """
    Класс для хранения всей информации о созданном пользователе.
    Содержит токен, данные пользователя и готовые API клиенты.
    """

    def __init__(self, token: str, details: UserResponseDto, password: str, client_factory: ClientFactory):
        self.token = token  # JWT токен для авторизации
        self.details = details  # Информация о пользователе
        self.password = password  # Пароль (для повторного логина)
        self.clients = client_factory  # Готовые API клиенты

        # Удобные свойства для быстрого доступа
        self.id = details.id
        self.username = details.username
        self.role = details.role


class UserBuilder:
    """
    Билдер для создания пользователей с разными ролями.

    Процесс создания:
    1. Регистрация через API
    2. Обновление роли через БД (если нужно)
    3. Авторизация для получения токена
    4. Создание фабрики API клиентов
    """

    def __init__(self, auth_api: AuthAPI, user_repo: UserRepository, base_url: str):
        self._auth_api = auth_api  # Клиент для авторизации
        self._user_repo = user_repo  # Репозиторий для работы с БД
        self._base_url = base_url  # Базовый URL API
        self._faker = Faker()  # Генератор тестовых данных

    @allure.step("Создание и аутентификация пользователя с ролью '{role}'")
    def create_user(self, role: str) -> User:
        """
        Создает пользователя с указанной ролью и возвращает готовый объект User.

        Args:
            role: Роль пользователя (CUSTOMER, SELLER, ADMIN)

        Returns:
            User: Объект с токеном и готовыми API клиентами
        """

        # Шаг 1: Генерируем уникальные данные для регистрации
        reg_request = RegisterRequest(
            username=f"{role.lower()}_{self._faker.user_name()}_{datetime.now().microsecond}",
            email=self._faker.email(),
            password=self._faker.password(length=12)
        )

        # Шаг 2: Регистрируем пользователя через API
        user_dto = self._auth_api.register(reg_request)

        # Шаг 3: Обновляем роль через БД (если не CUSTOMER)
        if role.upper() != "CUSTOMER":
            self._user_repo.update_role_by_id(user_dto.id, role)
            user_dto.role = role.upper()  # Обновляем локальный объект

        # Шаг 4: Авторизуемся для получения токена
        login_req = AuthRequest(
            username=reg_request.username,
            password=reg_request.password
        )
        auth_response = self._auth_api.login(login_req)

        # Шаг 5: Создаем фабрику API клиентов
        client_factory = ClientFactory(
            base_url=self._base_url,
            token=auth_response.token
        )

        # Шаг 6: Возвращаем готовый объект User
        return User(
            token=auth_response.token,
            details=user_dto,
            password=reg_request.password,
            client_factory=client_factory
        )