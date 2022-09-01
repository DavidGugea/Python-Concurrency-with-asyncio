import aiohttp
import asyncio


async def fetch(client):
    async with client.get('http://www.example.com') as resp:
        assert resp.status == 200
        return resp.status


async def main():
    async with aiohttp.ClientSession() as client:
        for _ in range(10):
            status_code = await fetch(client)
            print(status_code)


asyncio.run(main())
