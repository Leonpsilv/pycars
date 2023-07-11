import django_filters
from users.models import User


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    cpf = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = User
        fields = ["name", "email", "cpf"]
