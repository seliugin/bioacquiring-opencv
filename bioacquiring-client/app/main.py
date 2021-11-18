from aiohttp import web
from core import app
from asyncio import run, Event


async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()
    await Event().wait()

if __name__ == '__main__':
    run(main())

