from .celery import app

from rest.models import Word, Vacancies

from datetime import datetime
import requests


@app.task()
def check_out_vacancies():
    for word in Word.objects.all():
        s = requests.Session()
        cur_page = 0
        url = f'https://api.hh.ru/vacancies?text={word}&resume_search_fields=everywhere&per_page=100&page={cur_page}'
        headers = {'User-Agent': 'django_rest_api-test-agent'}
        vacansies = s.get(url, headers=headers).json()
        max_page = vacansies['pages']
        while cur_page <= max_page:
            for v in vacansies['items']:
                key_word = word
                title = v['name']
                # date = v['published_at']
                url = v['alternate_url']
                # id = v['id']
                try:
                    instance = Vacancies.objects.create(
                        key_word=key_word,
                        title=title,
                        date=datetime.today(),
                        # date=datetime.strptime(date.split('+')[0], '%Y-%m-%dT%X'),
                        url=url
                    )
                    instance.save()
                except Exception as e:
                    print(e)
                    continue
            url = f'https://api.hh.ru/vacancies?text={word}&resume_search_fields=everywhere&per_page=100&page={cur_page}'
            vacansies = s.get(url, headers=headers).json()
            max_page = vacansies['pages']
            cur_page = vacansies['page']
