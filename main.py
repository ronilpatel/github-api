import time
import logging
import sample_input as ei

from api.endpoint import ApiEndPoint
from sample_input import FILENAME, FILEPATH
from file_operations.filters import REPO_FILTERS
from file_operations.file_operation import CsvOperation
from api_requestor.requestor import AsyncApiRequestor

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')

logger = logging.getLogger('github-api-call')
logger.info('task started....')


def main():
    start = time.time()
    print('making api calls & writing to the file.......')

    # Preparing the API Endpoint
    endpoint = ApiEndPoint(url=ei.URL, params=dict(ei.PARAMS),
                           per_page=ei.PER_PAGE).endpoint

    # Returns a generator function to return api data
    requestor_obj = AsyncApiRequestor(endpoint=endpoint)
    api_data_generator_func = requestor_obj.make_api_calls()

    # Writing the repo records to csv file
    csv_obj = CsvOperation(columns=REPO_FILTERS)
    csv_obj.write_to_file(FILENAME, FILEPATH, api_data_generator_func)

    logger.info(f'Total time taken to complete: {time.time() - start}')
    logger.info('task ended....')
    print('Task ended! Please check log.txt for further information.......')


if __name__ == '__main__':
    main()
