import os
from unittest import TestCase
from unittest.mock import patch, mock_open
from sample_input import FILENAME, FILEPATH
from csv_writer.write_to_csv import CsvWriter
from csv_writer.filters import REPO_FILTERS


class TestCsvWriter(TestCase):

    def setUp(self) -> None:
        self.csv_writer_obj = CsvWriter(REPO_FILTERS)

    @patch('csv_writer.write_to_csv.csv.DictWriter.writerow')
    @patch("builtins.open", new_callable=mock_open, read_data="api-data")
    def test_write_to_file(self, mock_open_obj, mock_dict_row_writer_obj):
        def gen_func():
            z = [{key: key for key in REPO_FILTERS}]
            for item in z:
                yield item

        path_ = os.path.join(FILEPATH, f'{FILENAME}.csv')
        gen_func = gen_func()

        self.csv_writer_obj.write_to_file(FILENAME, FILEPATH, gen_func)

        mock_open_obj.assert_called_with(path_, encoding='utf-8', mode='w',
                                         newline='', )
        mock_dict_row_writer_obj.assert_called_with({key: key for key in
                                                     REPO_FILTERS})
