from datetime import datetime
from typing import Optional, Any, Dict, List

from tests.db.base_repo import BaseRepository


class MessageRepository(BaseRepository):
    """Репозиторий для работы с пользователями."""

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получает сообщения по ID."""
        row = self._db.fetchone(
            "SELECT * FROM messages WHERE sender_id = :sender_id",
            {"sender_id": user_id})
        return self._row_to_dict(row)


    def delete_by_id(self, user_id: int) -> None:
        """Удаляет сообщение по ID."""
        self._db.execute(
            "DELETE FROM messages WHERE sender_id = :sender_id",
            {"sender_id":user_id}
        )

    def create_by_id(self, sender_id: int, receiver_id: int, content: str) -> None:
        """Создаёт новое сообщение по ID."""
        self._db.execute(
            """
            INSERT INTO messages (sender_id, receiver_id, content, sent_at)
            VALUES (:sender_id, :receiver_id, :content, :sent_at)
            """,
            {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "content": content,
                "sent_at": datetime.utcnow()
            }
        )
