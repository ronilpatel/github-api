TEST_REQUEST_DATA = {"name": "Django",
                     "items": [{
                        "name": "github",
                        "description": "A repo",
                        "html_url": "https://abc.com",
                        "watchers_count": 3000,
                        "stargazers_count": 5000,
                        "forks_count": 5000}]}

TEST_ENDPOINT = 'https://api.github.com/search/repositories' \
                '?q=is:public+forks:>=2000+language:Python&page=5&per_page=100'

TEST_EXPECTED_DATA = [{
        "name": "github",
        "description": "A repo",
        "html_url": "https://abc.com",
        "watchers_count": 3000,
        "stargazers_count": 5000,
        "forks_count": 5000}]
