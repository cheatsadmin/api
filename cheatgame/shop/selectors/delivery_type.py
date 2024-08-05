from django.db.models import QuerySet

from cheatgame.shop.models import DeliveryType


def delivery_type_list() -> QuerySet[DeliveryType]:
    return DeliveryType.objects.all()
