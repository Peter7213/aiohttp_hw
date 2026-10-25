import asyncio

import aiohttp


async def main():

    async with aiohttp.ClientSession() as session:

        # resp = await session.post('http://127.0.0.1:8080/ads',
        #                           json={'header': 'Tesla car',
        #                                 'ad_body': 'bought to compensate for something',
        #                                 'owner': 'user_1'})
        # print(resp.status)
        # print(await resp.json())

        # resp = await  session.get('http://127.0.0.1:8080/ads/4')
        # print(resp.status)
        # print(await resp.json())

        # resp = await  session.patch('http://127.0.0.1:8080/ads/4',
        #                             json={'ad_body':'buy to flex on the poor'})
        # print(resp.status)
        # print(await resp.json())

        # resp = await  session.delete('http://127.0.0.1:8080/ads/4')
        # print(resp.status)
        # print(await resp.json())

asyncio.run(main())