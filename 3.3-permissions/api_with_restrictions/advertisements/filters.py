from django_filters import rest_framework as filters, DateFromToRangeFilter

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter()
    update_at = DateFromToRangeFilter()
    creator = filters.CharFilter(field_name='creator__id', lookup_expr='exact')
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)

    class Meta:
        model = Advertisement
        fields = ['created_at', 'update_at']
