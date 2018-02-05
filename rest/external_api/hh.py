import requests


class HeadHunterApi:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'django_rest_api-test-agent'}
        self.url = 'https://api.hh.ru/vacancies'

    def __create_url__(self, **kwargs):
        return ''.join((self.url, '?', '&'.join('{k}={v}'.format(k=k, v=v) for k, v in kwargs.items())))

    def hh_get_vacancies(self, retry=1, **kwargs):
        url = self.__create_url__(**kwargs)
        counter = 0
        while counter < retry:
            try:
                return self.session.get(url, headers=self.headers).json()
            except Exception as e:
                counter += 1
        else:
            raise e if retry > 0 else KeyError('Argument "retry" cannot be less then 1')
