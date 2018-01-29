from rest.views import WordViewSet, UserViewSet, VacanciesViewSet
from rest_framework import routers
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest.views import index
from django.contrib import admin

router = routers.SimpleRouter()
router.register(r'words', WordViewSet, base_name='word')
router.register(r'users', UserViewSet)
router.register(r'words/(?P<key_word>\d+)/vacancies', VacanciesViewSet),

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='homepage'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),

]
