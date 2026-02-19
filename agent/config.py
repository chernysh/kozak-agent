"""
Конфігурація агента з змінних середовища (.env).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Шукаємо .env у корені репозиторія (рівень вище agent/)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def _str_list(value: str) -> list[str]:
    if not value or not value.strip():
        return []
    return [m.strip() for m in value.split(",") if m.strip()]


def get_monitoring_url() -> str:
    return os.getenv("MONITORING_URL", "ws://localhost:8765").strip()


def get_api_key() -> str:
    return os.getenv("MONITORING_API_KEY", "").strip()


def get_enabled_modules() -> list[str]:
    return _str_list(os.getenv("ENABLED_MODULES", "ssh"))


def get_check_interval() -> int:
    return max(10, int(os.getenv("CHECK_INTERVAL", "60")))


# --- SSH ---
def get_ssh_host() -> str:
    return os.getenv("SSH_HOST", "localhost")


def get_ssh_port() -> int:
    return int(os.getenv("SSH_PORT", "22"))


def get_ssh_user() -> str:
    return os.getenv("SSH_USER", "root")


def get_ssh_key_path() -> str | None:
    p = os.getenv("SSH_KEY_PATH", "").strip()
    return p if p else None


def get_ssh_password() -> str | None:
    p = os.getenv("SSH_PASSWORD", "").strip()
    return p if p else None


# --- Postgres (заглушки для roadmap) ---
def get_postgres_host() -> str:
    return os.getenv("POSTGRES_HOST", "localhost")


def get_postgres_port() -> int:
    return int(os.getenv("POSTGRES_PORT", "5432"))


def get_postgres_user() -> str:
    return os.getenv("POSTGRES_USER", "monitor")


def get_postgres_password() -> str:
    return os.getenv("POSTGRES_PASSWORD", "")


def get_postgres_db() -> str:
    return os.getenv("POSTGRES_DB", "postgres")


# --- MySQL ---
def get_mysql_host() -> str:
    return os.getenv("MYSQL_HOST", "localhost")


def get_mysql_port() -> int:
    return int(os.getenv("MYSQL_PORT", "3306"))


def get_mysql_user() -> str:
    return os.getenv("MYSQL_USER", "monitor")


def get_mysql_password() -> str:
    return os.getenv("MYSQL_PASSWORD", "")


def get_mysql_database() -> str:
    return os.getenv("MYSQL_DATABASE", "mysql")


# --- Nginx ---
def get_nginx_status_url() -> str:
    return os.getenv("NGINX_STATUS_URL", "http://localhost/nginx_status")
