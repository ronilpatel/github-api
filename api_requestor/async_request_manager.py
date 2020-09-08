import json
import asyncio
import logging
import requests

from math import ceil
from api_requestor.async_requestor import get_multiple_request_data
from csv_writer.write_to_csv import CsvWriter
from csv_writer.filters import REPO_FILTERS
from sample_input import FILENAME, FILEPATH, PER_PAGE

logger = logging.getLogger('github-api-call.async_manager')


def filter_stargazers(item: dict) -> bool:
    if item.get('stargazers_count', '') and  \
            int(item['stargazers_count']) >= 2000:
        return True
    return False


def make_async_requests(endpoints: list):
    loop_var = asyncio.get_event_loop()
    logger.info('started making API calls...')
    request_data = loop_var.run_until_complete(get_multiple_request_data(
                                               loop_var, *endpoints))
    logger.info('All the api calls made!')
    try:
        x = [json.loads(data) for data in request_data]
    except json.decoder.JSONDecodeError:
        logger.warning('API data has single quotes. Double quotes expected!')
        x = []
    for item in x:
        for title in filter(filter_stargazers, item.get('items', '')):
            z = {key: title.get(key, '') for key in REPO_FILTERS}
            yield z


def write_records(endpoint: str):

    # Making api call to get the number of records
    response = requests.get(endpoint.format(page_number=1))
    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError:
        response_json = {}
    total_records = response_json.get('total_count', 0)
    total_api_calls = ceil(total_records/PER_PAGE)
    logger.info(f'Total api calls to be made : {total_api_calls}')

    # Make asynchronous requests
    endpoints = [endpoint.format(page_number=i+1)
                 for i in range(total_api_calls)]
    request_generator_func = make_async_requests(endpoints)

    # Writing the repo records to csv file
    csv_writer_obj = CsvWriter(columns=REPO_FILTERS)
    csv_writer_obj.write_to_file(FILENAME, FILEPATH, request_generator_func)
