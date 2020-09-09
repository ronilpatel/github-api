import csv
import os
import logging

from abc import ABCMeta, abstractmethod

logger = logging.getLogger('github-api-call.file_operations')


class FileOperation(metaclass=ABCMeta):
    """
    Handles the file operations to a file with a particular type
    eg. .csv, .xls, .txt etc.....
    """

    def __init__(self, extension):
        self.extension = extension

    @abstractmethod
    def write_to_file(self):
        pass

    @abstractmethod
    def read_from_file(self):
        pass


class CsvOperation(FileOperation):
    """
    Handles the file operations to a csv file
    """

    def __init__(self, columns: tuple):
        super().__init__('csv')
        self.columns = columns

    def write_to_file(self, filename, location, data_generator):
        path_ = os.path.join(location, f'{filename}.{self.extension}')
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
                        row = next(data_generator)
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

    def read_from_file(self):
        pass


class XlsOperation(FileOperation):
    """
    Handles the file operations to an xls file
    """

    def __init__(self, extension: str):
        super().__init__(extension)

    def write_to_file(self, filename, location, get_record_generator):
        pass

    def read_from_file(self):
        pass
