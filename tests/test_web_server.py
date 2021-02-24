from aiohttp import web
import pytest


from app.web_server import get_hello


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/', get_hello)
    return loop.run_until_complete(aiohttp_client(app))


async def test_get_hello(cli):
    resp = await cli.get('/')
    assert resp.status == 200
