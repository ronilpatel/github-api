import time
import logging
import sample_input as ei
from api.endpoint import ApiEndPoint
from api_requestor.async_request_manager import write_records

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')

logger = logging.getLogger('github-api-call')
logger.info('task started....')


def main():
    start = time.time()
    print('making api calls & writing to the file.......')
    endpoint = ApiEndPoint(url=ei.URL, params=dict(ei.PARAMS),
                           per_page=ei.PER_PAGE).endpoint
    write_records(endpoint)
    logger.info(f'Total time taken to complete: {time.time() - start}')
    logger.info('task ended....')
    print('task ended! Please check log.txt for further information.......')


if __name__ == '__main__':
    main()
