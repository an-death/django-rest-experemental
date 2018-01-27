import os
import sys
from django.conf import settings

####################################################################################
## SETTINGS
####################################################################################
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# use base_dir as import root
sys.path[0] = os.path.dirname(BASE_DIR)

# the current folder name will also be our app
APP_LABEL = os.path.basename(BASE_DIR)

settings.configure(
    DEBUG=os.environ.get('DEBUG', 'on') == 'on',
    SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(32)),
    ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS', 'localhost').split(','),
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.locale.LocaleMiddleware',
    ],
    INSTALLED_APPS=[
        APP_LABEL,
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
    ],
    STATIC_URL='/static/',
    STATICFILES_DIRS=[
        os.path.join(BASE_DIR, "static"),
    ],
    STATIC_ROOT=os.path.join(BASE_DIR, "static_root"),
    MEDIA_ROOT=os.path.join(BASE_DIR, "media"),
    MEDIA_URL='/media/',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "templates"), ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    REST_FRAMEWORK={
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAdminUser',
        ],
        'PAGE_SIZE': 10
    }
)
###################################################################################
##  SETTINGS END
###################################################################################

import django

django.setup()  # responsible for populating the application registry.

from django.contrib import admin
from django.db import models

###################################################################################
##  MODELS
###################################################################################
# Create your models here.

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True ,max_length=200)
    password = models.CharField(max_length=200)

    class Meta:
        app_label = APP_LABEL


class KeyWord(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=200, unique=True)
    users = models.ManyToManyField(User, 'words')

    class Meta:
        app_label = APP_LABEL


class Vacancies(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    ref = models.CharField(max_length=400)
    words = models.ManyToManyField(KeyWord, 'vacancies')


admin.site.register(User)
admin.site.register(KeyWord)
admin.site.register(Vacancies)
admin.autodiscover()

###################################################################################
##  MODELS END
###################################################################################

###################################################################################
## REST--API
###################################################################################
from rest_framework import serializers


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = '__all__'


from rest_framework import viewsets


class KeyWordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KeyWord.objects.all()
    serializer_class = KeyWordSerializer

#####################################################################################
## REST--API END
#####################################################################################

#####################################################################################
## URLS AND VIEWS
#####################################################################################

from django.conf.urls import url, include
from rest_framework import routers
from django.http import HttpResponse
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'kewords', KeyWordViewSet)


def index(request):
    """ index """
    return HttpResponse("Hello")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='homepage'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

######################################################################################
## URLS AND VIEWS END
######################################################################################

######################################################################################
## RUN
######################################################################################
from django.core.wsgi import get_wsgi_application


def return_application():
    return get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
else:
    return_application()
