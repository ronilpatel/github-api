from unittest import TestCase
from unittest.mock import patch, Mock
from api_requestor.requestor import AsyncApiRequestor
from api_requestor import async_request_manager as asym
from api_requestor.test_data import async_request_data as td


class TestAsyncApiRequestor(TestCase):

    def setUp(self) -> None:
        self.req_obj = AsyncApiRequestor(endpoint='')

    def test_filter_stargazers_correct(self):
        item = {
            'stargazers_count': 3000
        }
        self.assertTrue(self.req_obj.filter_stargazers(item))

    def test_filter_stargazers_incorrect(self):
        item = {
            'stargazers_count': 1500
        }
        self.assertFalse(self.req_obj.filter_stargazers(item))

    def test_filter_stargazers_absent(self):
        item = dict()
        self.assertFalse(self.req_obj.filter_stargazers(item))

    @patch('api_requestor.requestor.asyncio.get_event_loop')
    def test_make_async_requests_success(self, mock_obj):

        x = mock_obj.return_value
        y = [str(td.TEST_REQUEST_DATA).replace("'", '"')]
        x.run_until_complete.return_value = y
        generator_func = self.req_obj.make_async_requests(td.TEST_ENDPOINT)
        actual_data = list()
        while True:
            try:
                actual_data.append(next(generator_func))
            except StopIteration:
                break
        self.assertDictEqual(td.TEST_EXPECTED_DATA[0], actual_data[0])

    @patch('api_requestor.requestor.asyncio.get_event_loop')
    def test_make_async_requests_failure(self, mock_obj):

        x = mock_obj.return_value
        y = [str(td.TEST_REQUEST_DATA)]
        x.run_until_complete.return_value = y
        gen_function = asym.make_async_requests(td.TEST_ENDPOINT)
        actual_data = []
        while True:
            try:
                actual_data.append(next(gen_function))
            except StopIteration:
                break
        self.assertListEqual([], actual_data)

    @patch('api_requestor.requestor.requests.get')
    @patch('api_requestor.requestor.AsyncApiRequestor.make_async_requests')
    def test_make_api_calls(self, mock_async_req_obj, mock_request_obj):

        def fake_generator():
            repo = []
            for r in repo:
                yield r
        expected_value = fake_generator()
        mock_async_req_obj.return_value = expected_value

        json_response = {'total_count': 500}
        mock_request_obj.return_value = Mock(status_code=200)
        mock_request_obj.return_value.json.return_value = json_response

        request_gen_func = self.req_obj.make_api_calls()

        self.assertEqual(expected_value, request_gen_func)