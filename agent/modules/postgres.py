"""
Модуль перевірки зʼєднання з PostgreSQL.
Конфігурація з env: POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.
"""
from modules.base import BaseModule, CheckResult


class PostgresModule(BaseModule):
    name = "postgres"

    async def run(self) -> CheckResult:
        # TODO: реалізувати підключення (asyncpg) та просту перевірку (SELECT 1)
        return CheckResult(
            module=self.name,
            status="error",
            message="Модуль postgres ще не реалізовано",
            details={},
        )
