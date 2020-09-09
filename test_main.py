from main import main

from unittest import TestCase
from unittest.mock import patch
from sample_input import FILENAME, FILEPATH


class TestMain(TestCase):

    @patch('main.AsyncApiRequestor.make_api_calls')
    @patch('main.CsvOperation.write_to_file')
    def test_main(self, mock_write_to_file, mock_async_api_req):
        def fake_generator():
            repo = []
            for r in repo:
                yield r
        expected_value = fake_generator()
        mock_async_api_req.return_value = expected_value

        main()
        mock_async_api_req.assert_called_once()
        mock_write_to_file.assert_called_with(FILENAME, FILEPATH,
                                              expected_value)
