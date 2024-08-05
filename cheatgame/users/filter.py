from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from django_filters import CharFilter, FilterSet
from rest_framework.exceptions import APIException

from cheatgame.users.models import BaseUser


class UserFilter(FilterSet):
    search = CharFilter(method="filter_search")
    birthdate__range = CharFilter(method="filter_birthdate__range")
    created_at__range = CharFilter(method="filter_created_at__range")
    phone_number = CharFilter(method="filter_phone_number")
    email = CharFilter(method="filter_email")


    def filter_search(self, queryset, value , name):
        return queryset.annotate(search=SearchVector("lastname")).filter(search=name)


    def filter_birthdate__range(self, queryset, name, value):
        limit = 2
        birthdate__in = value.split(",")
        if len(birthdate__in) > limit:
            raise APIException("please just add two off_price with , in the middle")
        birthdate_0, birthdate_1 = birthdate__in if len(birthdate__in) else birthdate__in, None
        if not birthdate_1:
            return queryset.filter(birthdate__gte=birthdate_0[0])
        return queryset.filter(birthdate__range=(birthdate_0, birthdate_1))

    def filter_created_at__range(self, queryset, name, value):
        limit = 2
        created_at__in = value.split(",")
        if len(created_at__in) > limit:
            raise APIException("please just add two created_at with , in the middle")
        created_at_0, created_at_1 = created_at__in

        if not created_at_1:
            created_at_1 = timezone.now()

        if not created_at_0:
            return queryset.filter(created_at__date__lt=created_at_1)

        return queryset.filter(created_at__range=(created_at_0, created_at_1))

    def filter_phone_number(self, queryset, name, value):
        queryset = queryset.filter(phone_number=value)
        return queryset

    def filter_email(self , queryset, name, value):
        queryset = queryset.filter(email=value)
        return queryset






    class Meta:
        model = BaseUser
        fields = (
            "firstname",
            "lastname" ,
            "phone_number",
        )
