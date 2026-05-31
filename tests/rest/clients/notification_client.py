import requests

from tests.rest.core.http_client import HttpClient
from tests.rest.models.model import PageNotificationDto


class NotificationsAPI(HttpClient):
    """API клиент для работы с уведомлениями"""

    def get_all(self, params: dict = None) -> PageNotificationDto:
        """Получает уведомления пользователя"""
        return self._send_request(
            method="GET",
            path="/api/notifications",
            step_title="Получение уведомлений",
            params=params,
            expected_model=PageNotificationDto
        )

    def read(self, notification_id: int) -> requests.Response:
        """Помечает уведомление как прочитанное"""
        return self._send_request(
            method="PATCH",
            path=f"/api/notifications/{notification_id}/read",
            step_title=f"Пометка уведомления ID: {notification_id} как прочитанного"
        )

    def read_all(self) -> requests.Response:
        """Помечает все уведомления как прочитанные"""
        return self._send_request(
            method="PATCH",
            path="/api/notifications/read-all",
            step_title="Пометка всех уведомлений как прочитанных"
        )

    def delete_all(self) -> requests.Response:
        """Удаляет все уведомления пользователя"""
        return self._send_request(
            method="DELETE",
            path="/api/notifications",
            step_title="Удаление всех уведомлений"
        )