from tests.db.base_repo import BaseRepository
from typing import Optional, Dict, List, Any

class OrderRepository(BaseRepository):
    """Репозиторий для работы с заказами кофе."""

    def get_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        row = self._db.fetchone(
            "SELECT * FROM coffee_orders WHERE id = :id",
            {"id": order_id}
        )
        return self._row_to_dict(row)

    def get_all_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        rows = self._db.fetchall(
            "SELECT * FROM coffee_orders WHERE user_id = :user_id",
            {"user_id": user_id}
        )
        return self._rows_to_dicts(rows)

    def update_status(self, order_id: int, status: str) -> None:
        self._db.execute(
            """
            UPDATE coffee_orders
            SET status = :status
            WHERE id = :id
            """,
            {
                "status": status,
                "id": order_id
            }
        )