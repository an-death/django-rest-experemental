from django.contrib import admin
from rest.models import *

admin.site.register(Word)
admin.site.register(Vacancies)
admin.autodiscover()
