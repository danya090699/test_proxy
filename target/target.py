import asyncio
import logging
from aiohttp import web


app = web.Application()
logging.basicConfig(filename='requests.log', encoding='utf-8', level=logging.WARNING, format="%(asctime)s - %(message)s")
RESPONSE_TIME_SECONDS = 1
ACTIVE_REQUESTS = 0


async def index(request):
    global ACTIVE_REQUESTS
    ACTIVE_REQUESTS += 1
    await asyncio.sleep(RESPONSE_TIME_SECONDS)
    ACTIVE_REQUESTS -= 1
    return web.Response(text="hello")


async def log_active_requests_count():
    while True:
        await asyncio.sleep(10)
        logging.warning("active requests {}".format(ACTIVE_REQUESTS))


async def start_logging_active_requests_count(app):
    asyncio.create_task(log_active_requests_count())

app.router.add_get("/", index)
app.on_startup.append(start_logging_active_requests_count)
web.run_app(app, host="0.0.0.0", port=8000)
