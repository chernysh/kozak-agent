"""
Модуль перевірки SSH-зʼєднання.
Конфігурація з env: SSH_HOST, SSH_PORT, SSH_USER, SSH_KEY_PATH або SSH_PASSWORD.
"""
import asyncio
import logging
from typing import Any

from modules.base import BaseModule, CheckResult

from config import (
    get_ssh_host,
    get_ssh_key_path,
    get_ssh_password,
    get_ssh_port,
    get_ssh_user,
)

logger = logging.getLogger(__name__)


def _run_ssh_check_sync() -> tuple[bool, str, dict[str, Any]]:
    """Синхронна перевірка SSH (paramiko). Виконується в thread pool."""
    try:
        import paramiko
    except ImportError:
        return False, "paramiko не встановлено: pip install paramiko", {}

    host = get_ssh_host()
    port = get_ssh_port()
    user = get_ssh_user()
    key_path = get_ssh_key_path()
    password = get_ssh_password()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if key_path:
            client.connect(
                hostname=host,
                port=port,
                username=user,
                key_filename=key_path,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
            )
        elif password:
            client.connect(
                hostname=host,
                port=port,
                username=user,
                password=password,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
            )
        else:
            return False, "Не задано SSH_KEY_PATH або SSH_PASSWORD", {}
        client.close()
        return True, "SSH зʼєднання успішне", {"host": host, "port": port, "user": user}
    except Exception as e:
        return False, str(e), {"host": host, "port": port}


class SshModule(BaseModule):
    name = "ssh"

    async def run(self) -> CheckResult:
        loop = asyncio.get_event_loop()
        ok, message, details = await loop.run_in_executor(None, _run_ssh_check_sync)
        status = "ok" if ok else "error"
        return CheckResult(
            module=self.name,
            status=status,
            message=message,
            details=details,
        )
