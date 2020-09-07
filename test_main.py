from main import main

from unittest import TestCase
from unittest.mock import patch
from api.endpoint import ApiEndPoint
from sample_input import URL, PARAMS, PER_PAGE


class TestMain(TestCase):

    @patch('main.write_records')
    def test_main(self, mock_write_records_obj,):
        endpoint = ApiEndPoint(url=URL, params=dict(
            PARAMS), per_page=PER_PAGE).endpoint
        main()
        mock_write_records_obj.assert_called_with(endpoint)
