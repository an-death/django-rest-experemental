from celery.utils.log import get_task_logger
from .celery import app
from rest.models import Word, Vacancies
from rest.external_api.hh import HeadHunterApi

logger = get_task_logger(__name__)


@app.task
def check_out_vacancies():
    hh = HeadHunterApi()
    for word in Word.objects.all():
        logger.debug(f'Start Word: {word}')
        cur_page = 0
        vacancies = hh.hh_get_vacancies(text=word, resume_search_fields='everywhere', per_page=100, page=cur_page)
        max_page = int(vacancies['pages'])
        logger.debug(f'For word: {word} founded {vacancies["found"]} items, pages: {max_page}')
        while cur_page <= max_page:
            logger.debug(f'Start page: {cur_page}')
            for v in vacancies['items']:
                key_word = word
                title = v['name']
                url = v['alternate_url']
                logger.debug(f'Trying to save vacancies Title: {title}')
                not_saved = Vacancies.save_item(key_word=key_word, title=title, url=url)
                if not_saved:
                    logger.debug(f'Save failed. Reason: {not_saved}. Skip Title: {title}')
                    continue
                logger.debug(f'Title: {title} saved!')
            cur_page += 1
            logger.debug(f'Getting new data for page: {cur_page}')
            vacancies = hh.hh_get_vacancies(text=word, resume_search_fields='everywhere', per_page=100, page=cur_page)
            max_page = int(vacancies['pages'])
