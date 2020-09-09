import json
import time
import asyncio
import aiohttp
import logging
import requests
import async_timeout

from math import ceil
from sample_input import PER_PAGE
from file_operations.filters import REPO_FILTERS

logger = logging.getLogger('github-api-call.api_requestor_class')


class AsyncApiRequestor:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.loop_var = None
        self.session = None

    def make_api_calls(self):

        # Making api call to get the number of records
        response = requests.get(self.endpoint.format(page_number=1))
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            response_json = {}
        total_records = response_json.get('total_count', 0)
        total_api_calls = ceil(total_records / PER_PAGE)
        logger.info(f'Total api calls to be made : {total_api_calls}')

        # Make asynchronous requests
        endpoints = [self.endpoint.format(page_number=i+1)
                     for i in range(total_api_calls)]
        request_generator_func = self.make_async_requests(endpoints)

        return request_generator_func

    @staticmethod
    def filter_stargazers(item: dict) -> bool:
        if item.get('stargazers_count', '') and \
                int(item['stargazers_count']) >= 2000:
            return True
        return False

    def make_async_requests(self, endpoints):
        self.loop_var = asyncio.get_event_loop()
        logger.info('started making API calls...')
        request_data = self.loop_var.run_until_complete(
            self.get_multiple_request_data(*endpoints))
        logger.info('All the api calls made!')
        try:
            x = [json.loads(data) for data in request_data]
        except json.decoder.JSONDecodeError:
            logger.warning(
                'API data has single quotes. Double quotes expected!')
            x = []
        for item in x:
            for title in filter(self.filter_stargazers, item.get('items', '')):
                z = {key: title.get(key, '') for key in REPO_FILTERS}
                yield z

    async def get_multiple_request_data(self, *urls):
        async with aiohttp.ClientSession(loop=self.loop_var) as session:
            self.session = session
            tasks = [self.fetch_page(url) for url in urls]
            grouped_tasks = asyncio.gather(*tasks)
            return await grouped_tasks

    async def fetch_page(self, url):
        page_start = time.time()
        async with async_timeout.timeout(10):
            async with self.session.get(url) as response:
                logger.info(f'Time taken by page: {time.time() - page_start}')
                return await response.text(encoding='utf-8')
