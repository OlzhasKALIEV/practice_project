from typing import List

import requests

from tests.rest.core.http_client import HttpClient
from tests.rest.models.models import MessageRequestDto, MessageResponseDto


class MessagesAPI(HttpClient):
    """API клиент для работы с сообщениями"""

    def create(self, dto: MessageRequestDto) -> MessageResponseDto:
        """Создает новое сообщение"""
        return self._send_request(
            method="POST",
            path="/api/messages",
            step_title=f"Создание сообщения от {dto.senderId} к {dto.receiverId}",
            json=dto,
            expected_model=MessageResponseDto
        )

    def get_all(self) -> List[MessageResponseDto]:
        """Получает все сообщения"""
        return self._send_request(
            method="GET",
            path="/api/messages",
            step_title="Получение всех сообщений",
            expected_model=List[MessageResponseDto]
        )

    def get_by_id(self, message_id: int) -> MessageResponseDto:
        """Получает сообщение по ID"""
        return self._send_request(
            method="GET",
            path=f"/api/messages/{message_id}",
            step_title=f"Получение сообщения по ID: {message_id}",
            expected_model=MessageResponseDto
        )

    def get_by_sender(self, sender_id: int) -> List[MessageResponseDto]:
        """Получает все сообщения от отправителя"""
        return self._send_request(
            method="GET",
            path=f"/api/messages/sender/{sender_id}",
            step_title=f"Получение сообщений от отправителя ID: {sender_id}",
            expected_model=List[MessageResponseDto]
        )

    def get_by_receiver(self, receiver_id: int) -> List[MessageResponseDto]:
        """Получает все сообщения для получателя"""
        return self._send_request(
            method="GET",
            path=f"/api/messages/receiver/{receiver_id}",
            step_title=f"Получение сообщений для получателя ID: {receiver_id}",
            expected_model=List[MessageResponseDto]
        )

    def get_dialog(self, sender_id: int, receiver_id: int) -> List[MessageResponseDto]:
        """Получает диалог между двумя пользователями"""
        return self._send_request(
            method="GET",
            path=f"/api/messages/dialog/{sender_id}/{receiver_id}",
            step_title=f"Получение диалога между пользователями {sender_id} и {receiver_id}",
            expected_model=List[MessageResponseDto]
        )

    def delete(self, message_id: int) -> requests.Response:
        """Удаляет сообщение"""
        return self._send_request(
            method="DELETE",
            path=f"/api/messages/{message_id}",
            step_title=f"Удаление сообщения по ID: {message_id}"
        )