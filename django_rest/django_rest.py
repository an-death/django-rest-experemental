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
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
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
# DJANGO VALIDATORS
###################################################################################
from django.utils.translation import gettext_lazy
from rest_framework.exceptions import ValidationError

class LowerCaseUnique(object):
    def __init__(self, type):
        self.type = type
        self.error_message = gettext_lazy('Duplicate values are not allow')

    def __call__(self, field_data, all_data):
        for t in globals()[self.type].effective.all():
            if field_data.lower() == t.name:
                raise ValidationError(self.error_message)
###################################################################################
# DJANGO VALIDATORS END
###################################################################################

###################################################################################
#  MODELS
###################################################################################

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    key_word = models.CharField(max_length=200, unique=True, validators=[LowerCaseUnique])
    class Meta:
        app_label = APP_LABEL


class Vacancies(models.Model):
    key_word = models.ForeignKey(Word,on_delete=models.CASCADE, related_name='vacancies' )
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)

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
from rest_framework.permissions import IsAuthenticated, AllowAny
#
#
# class ActionBasedPermission(AllowAny):
#     def has_permission(self, request, view):
#         for klass, actions in getattr(view, 'action_permissions', {}).items():
#             if view.action in actions:
#                 return klass().has_permission(request, view)
#         return False

###################################################################################
# AUTHENTICATION END
###################################################################################

###################################################################################
# REST--API
###################################################################################
from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django_filters.rest_framework import DjangoFilterBackend


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WordSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        key_word = validated_data['key_word'].capitalize()
        try:
            instance = Word.objects.create(
                key_word=key_word
            )
            instance.save()
        except django.db.utils.IntegrityError:
            raise ValidationError(detail='{key_word: [ word with this key word already exists.]}',
                                  code=status.HTTP_400_BAD_REQUEST)
        return instance

    def destroy(self):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    class Meta:
        model = Word
        fields = ('key_word', 'id')


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    action_permissions = {
        IsAuthenticated: ['destroy', 'list', 'create', ],
        AllowAny: ['retrieve']
    }
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    @detail_route(permission_classes=[IsAuthenticated])
    def vacancies(self, request, id=None):
        word = Word.objects.get(pk=id)
        return Response(word.vacancies.all())

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

router = routers.SimpleRouter()
router.register(r'words', WordViewSet, base_name='word')
router.register(r'users', UserViewSet)


def index(request):
    """ index """
    return HttpResponse("Hello")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='homepage'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),
    # url(r'^words/P<pk>/vacancies/$', VacanciesViewSet.as_view({'get': 'list'}))

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
