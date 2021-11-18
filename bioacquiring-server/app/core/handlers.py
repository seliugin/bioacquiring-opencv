from aiohttp import web
from services import register, process

__all__ = ['routes']

routes = web.RouteTableDef()

@routes.post('/register')
async def register_handler(request: web.Request):
    json_data = await request.json()
    fdesc = json_data['fdesc']
    namehash = json_data['namehash']
    name = json_data['name']
    phone = json_data['phone']
    payment_token = json_data['payment_token']
    result = await register(fdesc,
                            namehash,
                            name,
                            phone,
                            payment_token)
    if result == 0:
        return web.Response(text='ok')
    elif result == 1:
        return web.Response(text='already')


@routes.post('/process')
async def process_handler(request: web.Request):
    json_data = await request.json()
    fdesc = json_data['fdesc']
    result = await process(fdesc)
    if result:
        return web.Response(text=f'ok{result}')
    else:
        return web.Response(text='not ok')