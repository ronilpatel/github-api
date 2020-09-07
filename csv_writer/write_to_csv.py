import csv
import os
import logging

logger = logging.getLogger('github-api-call.csv_writer')


class CsvWriter:
    """
    Handles the write operations to a csv file
    """
    EXTENSION = 'csv'

    def __init__(self, columns: tuple):
        self.columns = columns

    def write_to_file(self, filename, location, get_record_generator):

        path_ = os.path.join(location, f'{filename}.{self.EXTENSION}')
        try:
            logger.info('started writing to file........')
            # print('started writing to file........')
            with open(path_, mode='w', newline='', encoding='utf-8') as \
                    csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.columns)
                writer.writerow({key: key for key in self.columns})
                count = 0
                while True:
                    try:
                        row = next(get_record_generator)
                        writer.writerow(row)
                        count += 1
                    except StopIteration:
                        logger.info(f'Total rows written: {count}')
                        logger.info(f'File write Successful! File Path is: {path_}')
                        break
        except csv.Error:
            logger.critical('file writing failed!')
        except KeyError:
            logger.critical('file writing failed!')
