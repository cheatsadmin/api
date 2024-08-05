from django.db.models import QuerySet

from cheatgame.shop.models import DeliverySchedule


def get_list_of_delivery_schedule(* , from_date ,to_date, type) -> QuerySet[DeliverySchedule]:
    return DeliverySchedule.objects.filter(start__date__range= (from_date ,to_date), type = type)

