from aiohttp import web
from config import SECRET, WEBHOOK_ACCEPT, CONFIRMATION_TOKEN
from tortoise import Tortoise, run_async
import aiohttp_jinja2
import jinja2
from pathlib import Path
from global_settings import *
from tortoise_cfg import TORTOISE_ORM
from routes import actions, admin_realize, global_admin_realize, users_realize

index_dir = str(Path(__file__).resolve().parent)+'/index_page'


async def init():
    """
        INIT SQLITE3 DATABASE
    """
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

BOT.loop.run_until_complete(init())
BOT.set_blueprints(actions.bp, admin_realize.bp, global_admin_realize.bp, users_realize.bp)

app = web.Application()
routes = web.RouteTableDef()
if not WEBHOOK_ACCEPT:
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(index_dir)))
    app.router.add_static('/static/',
                          path=str('./index_page/'),
                          name='static')


@routes.get("/")
@aiohttp_jinja2.template('index.html')
async def hello(request):
    """
        ROOT SITE RESPONSE
    """
    return {}


@routes.get("/when_update")
@aiohttp_jinja2.template('whenupdate.html')
async def whenupdate(request):
    """
        WHENUPDATE SITE RESPONSE
    """
    return {}


@routes.get("/changelog")
@aiohttp_jinja2.template('changelog.html')
async def changelog(request):
    """
        WHENUPDATE SITE RESPONSE
    """
    return {}


@routes.post("/bot")
@routes.get("/bot")
async def bot_execute(request):
    """Bot request response"""
    if WEBHOOK_ACCEPT:
        return web.Response(text=CONFIRMATION_TOKEN)
    else:
        event = await request.json()
        emulation = await BOT.emulate(event, confirmation_token=CONFIRMATION_TOKEN, secret=SECRET)
        return web.Response(text=emulation)

app.add_routes(routes)
web.run_app(app, host="127.0.0.1", port=8033)
