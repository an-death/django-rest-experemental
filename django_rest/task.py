from django_rest.django_rest import Word, Vacancies
from datetime import datetime
import requests
from .django_rest import app


@app.task()
def check_out_vacancies():
    for word in Word.objects.all():
        s = requests.Session()
        url = f'https://api.hh.ru/vacancies?text={word}&resume_search_fields=everywhere'
        headers = {'User-Agent': 'django_rest_api-test-agent'}
        vacansies = iter(s.get(url, headers=headers).json())
        for v in vacansies:
            key_word = word.id
            title = v['name']
            date = v['created_at']
            url = v['alternate_url']
            # id = v['id']
            try:
                instance = Vacancies.objects.create(
                    key_word=key_word,
                    title=title,
                    date=datetime.strptime(date, '%Y-%m-%dT%X%z'),
                    url=url
                )
                instance.save()
            except Exception as e:
                print(e)
                continue
