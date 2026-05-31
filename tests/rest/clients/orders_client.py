from tests.rest.core.http_client import HttpClient
from tests.rest.models.models import CreateOrderDto, CoffeeOrderResponse, PageCoffeeOrderResponse, \
    UpdateOrderStatusRequest


class OrdersAPI(HttpClient):
    """API клиент для работы с заказами"""

    def create(self, dto: CreateOrderDto) -> CoffeeOrderResponse:
        """Создает новый заказ"""
        return self._send_request(
            method="POST",
            path="/api/orders",
            step_title="Создание заказа",
            json=dto,
            expected_model=CoffeeOrderResponse
        )

    def get_by_id(self, order_id: int) -> CoffeeOrderResponse:
        """Получает заказ по ID"""
        return self._send_request(
            method="GET",
            path=f"/api/orders/{order_id}",
            step_title=f"Получение заказа по ID: {order_id}",
            expected_model=CoffeeOrderResponse
        )

    def get_all(self, params: dict = None) -> PageCoffeeOrderResponse:
        """Получает список заказов с пагинацией"""
        return self._send_request(
            method="GET",
            path="/api/orders",
            step_title="Получение всех заказов",
            params=params,  # Для пагинации: {"page": 0, "size": 10}
            expected_model=PageCoffeeOrderResponse
        )

    def get_pending(self, params: dict = None) -> PageCoffeeOrderResponse:
        """Получает заказы в статусе ожидания"""
        return self._send_request(
            method="GET",
            path="/api/orders/pending",
            step_title="Получение заказов в ожидании",
            params=params,
            expected_model=PageCoffeeOrderResponse
        )

    def update_status(self, order_id: int, req: UpdateOrderStatusRequest) -> CoffeeOrderResponse:
        """Обновляет статус заказа (только для SELLER/ADMIN)"""
        return self._send_request(
            method="PUT",
            path=f"/api/orders/{order_id}/status",
            step_title=f"Обновление статуса заказа ID: {order_id} на '{req.status}'",
            json=req,
            expected_model=CoffeeOrderResponse
        )