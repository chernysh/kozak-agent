"""
Модуль перевірки Nginx (статус-сторінка або доступність).
Конфігурація з env: NGINX_STATUS_URL.
"""
from modules.base import BaseModule, CheckResult


class NginxModule(BaseModule):
    name = "nginx"

    async def run(self) -> CheckResult:
        # TODO: реалізувати GET до NGINX_STATUS_URL та парсинг
        return CheckResult(
            module=self.name,
            status="error",
            message="Модуль nginx ще не реалізовано",
            details={},
        )
