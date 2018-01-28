from django.db import models
from django_rest.settings import APP_LABEL
from datetime import datetime


class Word(models.Model):
    key_word = models.CharField(max_length=200, unique=True, validators=[LowerCaseUnique])

    class Meta:
        app_label = APP_LABEL


class Vacancies(models.Model):
    key_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='vacancies')
    date = models.DateTimeField(default=datetime.now())
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)

    class Meta:
        app_label = APP_LABEL
        unique_together = ('url', 'id')
        ordering = ['date']
