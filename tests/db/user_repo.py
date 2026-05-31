from typing import Optional, Dict, Any, List
from tests.db.base_repo import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий для работы с пользователями."""

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получает пользователя по ID."""
        row = self._db.fetchone("SELECT * FROM users WHERE id = :id", {"id": user_id})
        return self._row_to_dict(row)

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Получает пользователя по имени."""
        row = self._db.fetchone("SELECT * FROM users WHERE username = :username", {"username": username})
        return self._row_to_dict(row)

    def update_role_by_id(self, user_id: int, new_role: str) -> None:
        """Обновляет роль пользователя по ID."""
        self._db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": new_role.upper(), "id": user_id}
        )

    def get_all_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Получает всех пользователей с определенной ролью."""
        rows = self._db.fetchall("SELECT * FROM users WHERE role = :role", {"role": role.upper()})
        return self._rows_to_dicts(rows)