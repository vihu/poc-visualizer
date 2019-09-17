'''
Get all hotspots witness and receipt data.
'''

import requests
import asyncio
from aiohttp import ClientSession

BASE_URL = "https://alamo.helium.foundation/api"

async def fetch_witness(url, session, hotspot):
    '''
    Fetch witness for hotspot.
    '''
    async with session.get(url) as resp:
        response = await resp.json()
        hotspot.witnesses = len(response['data'])
        return hotspot

async def add_witnesses(hotspots):
    '''
    Add witnesses to hotspots.
    '''
    tasks = []

    async with ClientSession() as session:
        for hotspot in hotspots:
            url = f"{BASE_URL}/hotspots/{hotspot.addr}/witnesses"
            task = asyncio.ensure_future(fetch_witness(url, session, hotspot))
            tasks.append(task)

        await asyncio.gather(*tasks)

async def fetch_receipt(url, session, hotspot):
    '''
    Fetch receipt for hotspot.
    '''
    async with session.get(url) as resp:
        response = await resp.json()
        hotspot.receipts = len(response['data'])
        return hotspot

async def add_receipts(hotspots):
    '''
    Add receipts for hotspots.
    '''
    tasks = []

    async with ClientSession() as session:
        for hotspot in hotspots:
            url = f"{BASE_URL}/hotspots/{hotspot.addr}/receipts"
            task = asyncio.ensure_future(fetch_receipt(url, session, hotspot))
            tasks.append(task)

        await asyncio.gather(*tasks)

def append_witnesses_and_receipts(hotspots):
    '''
    Add witness and receipt data to hotspots.
    '''
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future1 = asyncio.ensure_future(add_witnesses(hotspots))
    future2 = asyncio.ensure_future(add_receipts(hotspots))
    loop.run_until_complete(future1)
    loop.run_until_complete(future2)
    return hotspots

if __name__ == '__main__':
    pass
