import os

PER_PAGE = 100
MAX_REQUESTS_LIMIT = 10

URL = 'https://api.github.com/search/repositories'

PARAMS = [
    ('is', 'public'),
    ('forks', '>=2000'),
    ('language', 'Python'),
]

FILENAME = 'github_api_data'
FILEPATH = os.path.abspath(os.path.curdir)
