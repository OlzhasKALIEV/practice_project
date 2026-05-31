from typing import Optional, Dict, Any, List

from sqlalchemy import Row

from tests.db.db_executor import DbExecutor


class BaseRepository:
    """Базовый класс для всех репозиториев с общей функциональностью."""

    def __init__(self, db_executor: DbExecutor):
        self._db = db_executor

    def _row_to_dict(self, row: Optional[Row]) -> Optional[Dict[str, Any]]:
        """Конвертирует Row в словарь или возвращает None."""
        return dict(row._mapping) if row else None

    def _rows_to_dicts(self, rows: List[Row]) -> List[Dict[str, Any]]:
        """Конвертирует список Row в список словарей."""
        return [dict(row._mapping) for row in rows]