import sys
import asyncio

from application import Application

if __name__ == '__main__':
    app = Application(sys.argv[1:])
    asyncio.run(app.run())
