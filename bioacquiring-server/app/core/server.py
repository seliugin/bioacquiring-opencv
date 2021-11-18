from aiohttp.web import Application
from core.handlers import routes

__all__ = ['app']

app = Application()
app.add_routes(routes)