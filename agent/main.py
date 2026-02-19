"""
Точка входу агента: періодично запускає увімкнені модулі та пушить результати в моніторинг.
"""
import asyncio
import logging
from datetime import datetime

from config import get_check_interval, get_enabled_modules
from client import push_to_monitoring
from modules import get_module

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def run_checks_and_push() -> None:
    """Запускає всі увімкнені модулі та відправляє результати в моніторинг."""
    enabled = get_enabled_modules()
    if not enabled:
        logger.warning("Немає увімкнених модулів (ENABLED_MODULES)")
        return
    for name in enabled:
        mod = get_module(name)
        if mod is None:
            logger.warning("Невідомий модуль: %s", name)
            continue
        try:
            result = await mod.run()
            await push_to_monitoring(result.to_payload())
        except Exception as e:
            logger.exception("Помилка модуля %s: %s", name, e)
            await push_to_monitoring({
                "type": "check",
                "module": name,
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            })


async def main_loop() -> None:
    interval = get_check_interval()
    logger.info("Агент стартував, інтервал перевірок: %s с", interval)
    while True:
        await run_checks_and_push()
        await asyncio.sleep(interval)


def main() -> None:
    asyncio.run(main_loop())


if __name__ == "__main__":
    main()
