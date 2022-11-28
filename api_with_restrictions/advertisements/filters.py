from django_filters import rest_framework as filters, DateFromToRangeFilter, AllValuesFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = DateFromToRangeFilter()
    status = AllValuesFilter(field_name='status')
    creator = AllValuesFilter(field_name='creator')
    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
