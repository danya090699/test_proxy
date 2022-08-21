import asyncio
import aiohttp
import subprocess

subprocess.run(["docker network create localnet"], check=True, shell=True)

subprocess.run(["docker build -t proxy:v1 ./proxy"], check=True, shell=True)
subprocess.run(["docker run -d --name proxy --net localnet -p 8000:8000 proxy:v1"], check=True, shell=True)

subprocess.run(["docker build -t target:v1 ./target"], check=True, shell=True)
with open("proxy/targets") as targets_addresses:
    for address in targets_addresses:
        target_name = address.split(":")[0]
        subprocess.run(["docker run -d --name {} --net localnet target:v1".format(target_name)], check=True, shell=True)


async def query(session):
    try:
        async with session.get('http://localhost:8000') as resp:
            x = await resp.text()
    except aiohttp.ClientConnectorError as e:
        print(str(e))


async def spam_with_queries():
    async with aiohttp.ClientSession() as session:
        for i in range(30000):
            asyncio.create_task(query(session))
            await asyncio.sleep(0.01)


async def temporary_disable_target():
    await asyncio.sleep(100)
    subprocess.run(["docker stop target1"], check=True, shell=True)
    await asyncio.sleep(100)
    subprocess.run(["docker restart target1"], check=True, shell=True)


async def main():
    await asyncio.gather(spam_with_queries(), temporary_disable_target())


asyncio.run(main())
