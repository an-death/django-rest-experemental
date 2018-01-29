import django_filters
from rest.models import Vacancies


class DTFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(name="date")

    class Meta:
        model = Vacancies
        fields = {
            'date': ['lte', 'gte', 'lt', 'gt'],
        }
