from aiohttp import web


async def get_hello(request):
    return web.Response(text='Hello, World!')


def run_web_server():
    app = web.Application()
    app.add_routes([web.get('/', get_hello)])
    web.run_app(app)
