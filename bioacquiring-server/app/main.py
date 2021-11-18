from aiohttp import web
from core import app
from database import init_db
from asyncio import run, Event
from database import init_db

async def main():
    await init_db()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()
    await Event().wait()

if __name__ == '__main__':
    run(main())

