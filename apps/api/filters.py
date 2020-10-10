import django_filters

from apps.api.models import Read


class ReadFilter(django_filters.FilterSet):
    timestamp__lte = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    timestamp__gt = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gt')

    class Meta:
        model = Read
        fields = ['timestamp__lte', 'timestamp__gt']
