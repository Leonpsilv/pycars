import django_filters
from cars.models import CarModel


class CarFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    brand = django_filters.CharFilter(lookup_expr="icontains")
    year = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.CharFilter(lookup_expr="icontains")
    # km = django_filters.CharFilter(lookup_expr="icontains")
    # price = django_filters.CharFilter(lookup_expr="icontains")
    color = django_filters.CharFilter(lookup_expr="icontains")
    new = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = CarModel
        fields = ["name", "brand", "year", "type", "color", "new"]
