"""
Фейковий моніторинг: WebSocket сервер, який приймає повідомлення від агента
і виводить їх у консоль. Для локальної розробки та тестування.
"""
import asyncio
import json
import logging
from datetime import datetime

import websockets
from websockets.server import serve

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

HOST = "0.0.0.0"
PORT = 8765


async def handler(websocket):
    """Обробляє кожне підключення: логує всі вхідні повідомлення."""
    client = websocket.remote_address
    logger.info("Нове підключення: %s", client)
    try:
        async for message in websocket:
            ts = datetime.utcnow().isoformat() + "Z"
            try:
                data = json.loads(message)
                logger.info(
                    "[WS] %s | від %s | JSON: %s",
                    ts,
                    client,
                    json.dumps(data, ensure_ascii=False, indent=2),
                )
            except json.JSONDecodeError:
                logger.info("[WS] %s | від %s | RAW: %s", ts, client, message)
    except websockets.exceptions.ConnectionClosed as e:
        logger.info("Зʼєднання закрито: %s — %s", client, e.reason)
    finally:
        logger.info("Клієнт відʼєднався: %s", client)


async def main():
    async with serve(handler, HOST, PORT, ping_interval=20, ping_timeout=20):
        logger.info("Фейковий моніторинг слухає ws://%s:%s", HOST, PORT)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
