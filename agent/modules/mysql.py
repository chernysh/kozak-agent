"""
Модуль перевірки зʼєднання з MySQL/MariaDB.
Конфігурація з env: MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE.
"""
from modules.base import BaseModule, CheckResult


class MysqlModule(BaseModule):
    name = "mysql"

    async def run(self) -> CheckResult:
        # TODO: реалізувати підключення (aiomysql) та перевірку
        return CheckResult(
            module=self.name,
            status="error",
            message="Модуль mysql ще не реалізовано",
            details={},
        )
