import allure
import pytest

from tests.rest.models.model import CreateOrderDto, UpdateOrderStatusRequest

from tests.db.ingredient_repo import IngredientRepository
from tests.db.orders_repo import OrderRepository
from tests.helpers.user_builder import UserBuilder


@pytest.mark.orders
@allure.feature("Сквозной сценарий работы с заказом")
class TestOrderWorkflow:

    @allure.story("Полный цикл: Создание заказа -> Проверка в БД -> Уведомления")
    def test_full_order_cycle(
            self,
            user_builder: UserBuilder,
            managed_ingredients,
            ingredient_repository: IngredientRepository,
            order_repository: OrderRepository
    ):
        # --- ARRANGE ---
        with allure.step("Подготовка: Создание Покупателя и Продавца"):
            customer = user_builder.create_user(role="CUSTOMER")
            seller = user_builder.create_user(role="SELLER")

        with allure.step("Подготовка: Создание ингредиента"):
            ingredient_id = managed_ingredients(count=1, quantity=2)[0]

        # --- ACT: Создание заказа ---
        with allure.step("ACTION: Покупатель создает заказ"):
            order_comment = "Пожалуйста, побыстрее!"
            order_payload = CreateOrderDto(
                ingredientIds=[ingredient_id],
                comment=order_comment
            )
            created_order_response = customer.clients.orders.create(order_payload)

        # --- УЛУЧШЕННЫЕ ПРОВЕРКИ ЧЕРЕЗ БД ---
        with allure.step("ASSERT: Заказ корректно записан в базу данных"):
            # Напрямую достаем запись о заказе из БД
            order_from_db = order_repository.get_by_id(created_order_response.id)

            assert order_from_db is not None, "Заказ не найден в БД после создания через API!"
            # Сравниваем ключевые поля
            assert order_from_db['user_id'] == customer.id, "В заказе неверный ID пользователя"
            assert order_from_db['status'] == "CREATED", "В заказе неверный начальный статус"
            assert order_from_db['comment'] == order_comment, "В заказе неверный комментарий"

        # ... (остальные проверки: уменьшение количества ингредиентов, уведомления и т.д.) ...

        with allure.step("ACTION: Продавец меняет статус заказа на INPROGRESS"):
            status_update_payload = UpdateOrderStatusRequest(status="INPROGRESS")
            seller.clients.orders.update_status(created_order_response.id, status_update_payload)

        with allure.step("ASSERT: Статус заказа в БД изменился на INPROGRESS"):
            # Снова проверяем напрямую в БД
            updated_order_from_db = order_repository.get_by_id(created_order_response.id)
            assert updated_order_from_db['status'] == "INPROGRESS", "Статус заказа в БД не обновился"


def test_order_creation(user_builder, managed_ingredients):
    customer = user_builder.create_user("CUSTOMER")

    # Создаем 3 ингредиента по 2 штуки каждый
    ingredient_ids = managed_ingredients(count=3, quantity=2)

    # Создаем заказ с этими ингредиентами
    order = customer.clients.orders.create(
        CreateOrderDto(ingredientIds=ingredient_ids)
    )

    assert len(order.ingredients) == 3
    # После теста ингредиенты автоматически удалятся

