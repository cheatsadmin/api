from typing import List

from django.db import transaction
from django.db.models import QuerySet, F

from cheatgame.shop.models import DeliverySchedule, DeliveryType, DeliveryData
from cheatgame.users.models import Address


def create_delivery_schedule(*, delivery_schedule: List[DeliverySchedule]) -> QuerySet[DeliverySchedule]:
    return DeliverySchedule.objects.bulk_create(delivery_schedule)


def update_delivery_schedule(*, id, type: int, start, end, capacity) -> DeliverySchedule:
    delivery_schedule = DeliverySchedule.objects.get(id=id)
    delivery_schedule.type = type
    delivery_schedule.start = start
    delivery_schedule.end = end
    delivery_schedule.capacity = capacity
    delivery_schedule.save()
    return delivery_schedule


def delete_delivery_schedule(*, delivery_schedule_id: id) -> None:
    DeliverySchedule.objects.get(id=delivery_schedule_id).delete()


def decrease_capacity_delivery_schedule(delivery_schedule: DeliverySchedule) -> None:
    delivery_schedule.capacity = F("capacity") - 1
    delivery_schedule.save()


@transaction.atomic
def create_schedule_data(*, type: DeliveryType, schedule: DeliverySchedule, address: Address) -> DeliveryData:
    decrease_capacity_delivery_schedule(delivery_schedule=schedule)
    return DeliveryData.objects.create(type=type, schedule=schedule, address=address)
