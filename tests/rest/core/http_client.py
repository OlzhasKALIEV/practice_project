import allure
import json
import logging
import requests
from typing import Union, Type, TypeVar, Any
from allure_commons.types import AttachmentType
from pydantic import BaseModel, ValidationError, TypeAdapter

logger = logging.getLogger(__name__)

T = TypeVar("T")


class HttpClient:

    def __init__(self, base_url: str, token: Union[str, None] = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        # Настраиваем заголовки по умолчанию
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

        if token:
            self.set_token(token)

    def set_token(self, token: str):
        """Устанавливает токен авторизации"""
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.debug(f"Установлен токен авторизации: {token[:10]}...")

    def _send_request(
            self,
            method: str,
            path: str,
            step_title: str,
            expected_model: Type[T] = None,
            **kwargs: Any
    ) -> Union[T, requests.Response]:
        """
        Центральный метод для отправки всех запросов.
        Выполняет:
        - Создание шага в Allure
        - Детальное логирование
        - Аттачи запроса/ответа
        - Валидацию статус-кода
        - Парсинг в Pydantic модель
        """
        with allure.step(step_title):
            url = f"{self.base_url}{path}"

            # Если передана Pydantic модель, конвертирует в словарь
            if 'json' in kwargs and isinstance(kwargs['json'], BaseModel):
                kwargs['json'] = kwargs['json'].model_dump(by_alias=True, exclude_none=True)

            # Логируем запрос
            logger.info(f"--> {method} {url}")
            if 'params' in kwargs:
                logger.info(f" Query params: {kwargs['params']}")

            # Отправляем запрос
            try:
                response = self.session.request(method, url, **kwargs)
                request = response.request

                # Аттачи для Allure
                allure.attach(
                    f"{request.method} {request.url}",
                    name="🌐 Request Endpoint",
                    attachment_type=AttachmentType.TEXT
                )

                # Аттачим тело запроса
                if request.body:
                    try:
                        body_str = request.body.decode('utf-8') if isinstance(request.body, bytes) else str(
                            request.body)
                        body_json = json.loads(body_str)
                        pretty_body = json.dumps(body_json, indent=2, ensure_ascii=False)
                        allure.attach(pretty_body, name="📤 Request Body", attachment_type=AttachmentType.JSON)
                        logger.info(f" Request Body: {pretty_body}")
                    except Exception:
                        logger.info(f" Request Body (raw): {request.body}")

                # Логируем ответ
                logger.info(f"<-- {response.status_code} {response.reason}")
                allure.attach(
                    f"{response.status_code} {response.reason}",
                    name="📊 Response Status",
                    attachment_type=AttachmentType.TEXT
                )

                # Аттачим тело ответа
                try:
                    response_json = response.json()
                    pretty_response = json.dumps(response_json, indent=2, ensure_ascii=False)
                    allure.attach(pretty_response, name="📥 Response Body", attachment_type=AttachmentType.JSON)
                    logger.info(f" Response Body: {pretty_response}")
                except json.JSONDecodeError:
                    if response.text:
                        allure.attach(response.text, name="📥 Response Body", attachment_type=AttachmentType.TEXT)
                        logger.info(f" Response Body (text): {response.text}")

                # Проверяем статус код
                response.raise_for_status()

                # Парсим в модель, если указана
                if expected_model and response.text:
                    try:
                        adapter = TypeAdapter(expected_model)
                        parsed_result = adapter.validate_python(response.json())
                        return parsed_result
                    except ValidationError as e:
                        allure.attach(str(e), name="❌ Pydantic Validation Error", attachment_type=AttachmentType.TEXT)
                        raise

                return response

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Ошибка HTTP запроса: {e}")
                allure.attach(str(e), name="❌ HTTP Error", attachment_type=AttachmentType.TEXT)
                raise

    def close(self):
        """Закрывает сессию"""
        self.session.close()
        logger.debug("HTTP сессия закрыта")