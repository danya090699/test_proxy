import aiohttp
from aiohttp import web


TARGET_TO_ACTIVE_REQUESTS = dict()

with open("targets") as targets_addresses:
    for address in targets_addresses:
        TARGET_TO_ACTIVE_REQUESTS[address] = 0


async def index(request):
    global TARGET_TO_ACTIVE_REQUESTS
    targets_down = []  # список таргетов, которые не отвечают в данный момент
    for i in range(2):  # 2 попытки сделать запрос
        # ищем наименее загруженный таргет
        least_loaded_target = None
        for target, active_requests in TARGET_TO_ACTIVE_REQUESTS.items():
            if target not in targets_down and (least_loaded_target is None or TARGET_TO_ACTIVE_REQUESTS[least_loaded_target] > active_requests):
                least_loaded_target = target
        # отправляем запрос в него
        async with aiohttp.ClientSession() as session:
            try:
                TARGET_TO_ACTIVE_REQUESTS[least_loaded_target] += 1
                async with session.get('http://{}'.format(least_loaded_target)) as resp:
                    TARGET_TO_ACTIVE_REQUESTS[least_loaded_target] -= 1
                    text = await resp.text()
                    return web.Response(text=text)
            except aiohttp.ClientConnectorError as e:
                TARGET_TO_ACTIVE_REQUESTS[least_loaded_target] -= 1
                targets_down.append(least_loaded_target)


app = web.Application()
app.router.add_get("/", index)
web.run_app(app, host="0.0.0.0", port=8000)
