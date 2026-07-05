import sys
import asyncio

# Кросс-платформенная настройка asyncio
if sys.platform == 'win32':
    # Для Windows используем Proactor (поддерживает subprocess)
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except AttributeError:
        # Для старых версий Python
        pass

__version__ = "3.1.0"
__author__ = "lixynhay"