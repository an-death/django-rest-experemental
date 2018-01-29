import requests
from celery.utils.log import get_task_logger

from .celery import app
from rest.models import Word, Vacancies

logger = get_task_logger(__name__)


@app.task
def check_out_vacancies():
    for word in Word.objects.all():
        logger.debug(f'Start Word: {word}')
        s = requests.Session()
        cur_page = 0
        url = f'https://api.hh.ru/vacancies?text={word}&resume_search_fields=everywhere&per_page=100&page={cur_page}'
        headers = {'User-Agent': 'django_rest_api-test-agent'}
        vacansies = s.get(url, headers=headers).json()
        max_page = int(vacansies['pages'])
        logger.debug(f'For word: {word} founded {vacansies["found"]} items, pages: {max_page}')
        while cur_page <= max_page:
            logger.debug(f'Start page: {cur_page}')
            for v in vacansies['items']:
                key_word = word
                title = v['name']
                # date = v['published_at']
                url = v['alternate_url']
                # id = v['id']
                logger.debug(f'Trying to save vacancies Title: {title}')
                try:
                    instance = Vacancies.objects.create(
                        key_word=key_word,
                        title=title,
                        # date=datetime.today(),
                        # date=datetime.strptime(date.split('+')[0], '%Y-%m-%dT%X'),
                        url=url
                    )
                    instance.save()
                except Exception as e:
                    logger.debug(f'Save failed. Reason: {e}. Skip Title: {title}')
                    continue
                logger.debug(f'Title: {title} saved!')
            cur_page += 1
            logger.debug(f'Getting new data for page: {cur_page}')
            url = f'https://api.hh.ru/vacancies?text={word}&resume_search_fields=everywhere&per_page=100&page={cur_page}'
            vacansies = s.get(url, headers=headers).json()
            max_page = vacansies['pages']
