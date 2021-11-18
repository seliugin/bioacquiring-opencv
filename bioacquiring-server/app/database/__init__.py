import core.settings as settings
from .models import db

__all__ = ['db', 'init_db']

async def init_db():
    await db.set_bind(f'postgresql://{settings.DATABASE["USER"]}:{settings.DATABASE["PASSWORD"]}'
                      f'@{settings.DATABASE["HOST"]}:{settings.DATABASE["PORT"]}/{settings.DATABASE["NAME"]}')

