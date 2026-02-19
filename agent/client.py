"""
Клієнт для відправки даних на моніторинг по WebSocket.
"""
import asyncio
import json
import logging
from typing import Any

import websockets

from config import get_api_key, get_monitoring_url

logger = logging.getLogger(__name__)


async def push_to_monitoring(payload: dict[str, Any]) -> bool:
    """
    Відправляє один JSON-обʼєкт на моніторинг.
    payload може містити type, module, status, message, metrics, timestamp тощо.
    """
    url = get_monitoring_url()
    api_key = get_api_key()
    if api_key:
        payload["api_key"] = api_key
    body = json.dumps(payload, ensure_ascii=False)
    try:
        async with websockets.connect(url, ping_interval=20, ping_timeout=10) as ws:
            await ws.send(body)
            logger.debug("Відправлено на моніторинг: %s", payload.get("type", "event"))
            return True
    except Exception as e:
        logger.warning("Не вдалося відправити на моніторинг: %s", e)
        return False


async def push_events_loop(queue: asyncio.Queue) -> None:
    """
    Фонова задача: бере події з черги та відправляє їх на моніторинг.
    Дозволяє не блокувати модулі перевірки.
    """
    while True:
        try:
            payload = await queue.get()
            await push_to_monitoring(payload)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.exception("Помилка відправки події: %s", e)
