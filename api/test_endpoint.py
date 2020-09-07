from unittest import TestCase
from api.endpoint import ApiEndPoint


class TestApiEndpoint(TestCase):

    def setUp(self) -> None:
        url = 'https://api.github.com/search/repositories'
        params = dict([('is', 'public'),
                       ('forks', '>=2000'),
                       ('language', 'Python')])
        per_page = 100
        self.api_endpoint_obj = ApiEndPoint(url, params, per_page)

    def test_endpoint_with_query_parameters_result_correct(self):
        expected_endpoint = 'https://api.github.com/search/repositories?q=is' \
                      ':public+forks:>=2000+language:Python'
        self.assertEqual(expected_endpoint,
                         self.api_endpoint_obj.endpoint_with_query_parameters)

    def test_endpoint_with_query_parameters_result_incorrect(self):
        expected_endpoint = 'https://api.github.com/search/repositories?q=is' \
                      ':public+forks:%3E2000+language:Python'
        self.assertNotEqual(expected_endpoint,
                            self.api_endpoint_obj.endpoint_with_query_parameters)

    def test_endpoint_correct(self):
        expected_endpoint = 'https://api.github.com/search/repositories' \
                            '?q=is:public+forks:>=2000+language:Python' \
                            '&page=5&per_page=100'
        actual_endpoint = self.api_endpoint_obj.endpoint.format(page_number=5)
        self.assertEqual(expected_endpoint, actual_endpoint)

    def test_endpoint_incorrect(self):
        expected_endpoint = 'https://api.github.com/search/repositories' \
                            '?q=is:public+forks:>=2000+language:Python' \
                            '&per_page=100&page=5'
        actual_endpoint = self.api_endpoint_obj.endpoint.format(page_number=5)
        self.assertNotEqual(expected_endpoint, actual_endpoint)
