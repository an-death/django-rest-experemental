from django.http import HttpResponse
from django.db.utils import IntegrityError
import json


def index(request):
    """ index """
    return HttpResponse("Hello")


###################################################################################
# REST--API
###################################################################################
from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import list_route, detail_route
from django_filters.rest_framework import DjangoFilterBackend

from rest.models import Word, Vacancies
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = ('title', 'id', 'url')


class VacanciesViewSet(viewsets.ModelViewSet):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer


class WordSerializer(serializers.ModelSerializer):
    vacancies = VacanciesSerializer(many=True, read_only=True)

    def create(self, validated_data):
        key_word = validated_data['key_word'].capitalize()
        try:
            instance = Word.objects.create(
                key_word=key_word
            )
            instance.save()
        except IntegrityError:
            raise ValidationError(detail=json.loads('{"key_word": ["word with this key word already exists."]}'),
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
        fields = ('key_word', 'id', 'vacancies')
        extra_kwargs = {'vacancies': {'lookup_field': 'id', 'view_name': 'words-vacancies'}}


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
        word = WordSerializer(instance=Word.objects.get(pk=id))
        return Response(word.data.get('vacancies'))
