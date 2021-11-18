
from aiohttp import web, WSMsgType
from .process import get_frames

__all__ = ['routes']

routes = web.RouteTableDef()

@routes.get('/stream')
async def stream_handler(request: web.Request):
    mode = request.query['mode']
    response = web.StreamResponse()
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    await response.prepare(request)
    for frame in get_frames(mode, request):
        await response.write(frame)
    return response

@routes.get('/status')
async def state_handler(request: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare()
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws