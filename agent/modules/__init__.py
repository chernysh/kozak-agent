"""
Модулі перевірок: кожен модуль відповідає за один тип сервісу/зʼєднання.
"""
from modules.base import BaseModule, CheckResult
from modules.ssh import SshModule
from modules.postgres import PostgresModule
from modules.mysql import MysqlModule
from modules.nginx import NginxModule

REGISTRY: dict[str, type[BaseModule]] = {
    "ssh": SshModule,
    "postgres": PostgresModule,
    "mysql": MysqlModule,
    "nginx": NginxModule,
}


def get_module(name: str) -> BaseModule | None:
    cls = REGISTRY.get(name)
    return cls() if cls else None
