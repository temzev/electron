# MANAGER
import sys
# stop the python from creating .pyc files
sys.dont_write_bytecode = True

from application.engine.router import Router
import asyncio


try:
    asyncio.run(main = Router().runner())
except KeyboardInterrupt:
    print("\r\033[91mServer Stopped!\033[0m")
