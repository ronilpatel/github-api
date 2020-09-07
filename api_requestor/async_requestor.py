import aiohttp
import asyncio
import async_timeout
import logging
import time

logger = logging.getLogger('github-api-call.async_requestor')


async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            logger.info(f'Time taken by page: {time.time()-page_start}')
            return await response.text(encoding='utf-8')


async def get_multiple_request_data(loop, *urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [fetch_page(session, url) for url in urls]
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks
