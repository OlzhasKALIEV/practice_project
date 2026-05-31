from typing import Optional, Dict, List, Any

from tests.db.base_repo import BaseRepository


class IngredientRepository(BaseRepository):
    """Репозиторий для работы с ингредиентами."""

    def get_by_id(self, ingredient_id: int) -> Optional[Dict[str, Any]]:
        """Получает ингредиент по ID."""
        row = self._db.fetchone("SELECT * FROM ingredients WHERE id = :id", {"id": ingredient_id})
        return self._row_to_dict(row)

    def get_all(self) -> List[Dict[str, Any]]:
        """Получает все ингредиенты."""
        rows = self._db.fetchall("SELECT * FROM ingredients ORDER BY name")
        return self._rows_to_dicts(rows)

    def update_quantity(self, ingredient_id: int, new_quantity: int) -> None:
        """Обновляет количество ингредиента."""
        self._db.execute(
            "UPDATE ingredients SET quantity = :quantity WHERE id = :id",
            {"quantity": new_quantity, "id": ingredient_id}
        )