from cheatgame.shop.models import DeliveryType


def create_delivery_type(*, name: str, delivery_type: int, side: int) -> DeliveryType:
    return DeliveryType.objects.create(
        name=name,
        delivery_type=delivery_type,
        side=side
    )


def update_delivery_type(*, delivery_type_id: id, name: str, delivery_type: int, side: int) -> DeliveryType:
    return DeliveryType.objects.filter(id=delivery_type_id).update(
        name=name,
        delivery_type=delivery_type,
        side=side
    )


def delete_delivery_type(*, delivery_type_id: int) -> None:
    DeliveryType.objects.get(id=delivery_type_id).delete()
