import os
import sys
from django.conf import settings

####################################################################################
# SETTINGS
####################################################################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# use base_dir as import root
sys.path[0] = os.path.dirname(BASE_DIR)

# the current folder name will also be our app
APP_LABEL = os.path.basename(BASE_DIR)

settings.configure(
    DEBUG=os.environ.get('DEBUG', 'on') == 'on',
    SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(32)),
    ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(','),
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
        'rest_framework.authtoken',
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
        'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        ),
        'PAGE_SIZE': 10
    }
)


import django

django.setup()  # responsible for populating the application registry.


###################################################################################
#  SETTINGS END
###################################################################################

###################################################################################
#  MODELS
###################################################################################

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=200, unique=True)
    class Meta:
        app_label = APP_LABEL


class Vacancies(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    words = models.ManyToManyField(Word, 'vacancies')

    class Meta:
        app_label = APP_LABEL


admin.site.register(Word)
admin.site.register(Vacancies)
admin.autodiscover()

###################################################################################
#  MODELS END
###################################################################################

###################################################################################
# AUTHENTICATION
###################################################################################
from rest_framework.authtoken.views import obtain_auth_token

###################################################################################
# AUTHENTICATION END
###################################################################################

###################################################################################
# REST--API
###################################################################################
from rest_framework import serializers
from rest_framework import viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('keyword', 'id')

    def create(self, validated_data):
        word = Word.objects.create(
            word=validated_data['keyword'],
        )
        word.save()

    def delete(self, ):
        pass

class WordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class VacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = ('title', 'id', 'url')

class VacanciesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer


#####################################################################################
# REST--API END
#####################################################################################

#####################################################################################
# URLS AND VIEWS
#####################################################################################

from django.conf.urls import url, include
from rest_framework import routers
from django.http import HttpResponse
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'words', WordViewSet)
router.register(r'users', UserViewSet)
router.register(r'vacancies', VacanciesViewSet)

def index(request):
    """ index """
    return HttpResponse("Hello")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='homepage'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),
]

######################################################################################
# URLS AND VIEWS END
######################################################################################

######################################################################################
# MAIN
######################################################################################
from django.core.wsgi import get_wsgi_application


def return_application():
    return get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
else:
    return_application()
