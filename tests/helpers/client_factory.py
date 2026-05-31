from tests.rest.clients.ingridient_client import IngredientsAPI
from tests.rest.clients.message_client import MessagesAPI
from tests.rest.clients.notification_client import NotificationsAPI
from tests.rest.clients.orders_client import OrdersAPI
from tests.rest.clients.users_client import UsersAPI


class ClientFactory:
    """
    Фабрика API клиентов для аутентифицированного пользователя.
    Создает все необходимые клиенты с правильным токеном авторизации.
    """

    def __init__(self, base_url: str, token: str):
        # Создаем все клиенты сразу при инициализации фабрики
        self.orders = OrdersAPI(base_url, token=token)
        self.notifications = NotificationsAPI(base_url, token=token)
        self.ingredients = IngredientsAPI(base_url, token=token)
        self.messages = MessagesAPI(base_url, token=token)
        self.users = UsersAPI(base_url, token=token)