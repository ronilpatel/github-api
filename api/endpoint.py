import logging

logger = logging.getLogger('github-api-call.api_endpoint_cls')


class ApiEndPoint:
    """"
    Defines an API endpoint along with other endpoint parameters
    """

    def __init__(self, url: str, params: dict, per_page: int):
        self.url = url
        self.params = params
        self.per_page = per_page

    def __repr__(self):
        return f'<ApiEndPoint {self.url}, {self.params}, {self.per_page}>'

    @property
    def endpoint_with_query_parameters(self):
        return self.url.rstrip('/') + '?q=' + '+'.join([
            f'{key}:{value}' for key, value in self.params.items()])

    @property
    def endpoint(self):
        return '&'.join([self.endpoint_with_query_parameters,
                         'page={page_number}', f'per_page={self.per_page}'])
