import datetime
import decimal
import secrets

from django.db import transaction

from cheatgame.shop.models import Discount
from cheatgame.users.models import BaseUser


def generate_code(discount_id: str) -> str:
    upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
    random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
    code = (random_str + discount_id)[-8:]
    return code


@transaction.atomic
def create_discount(*, name: str, type: int, value_type: int, valid_from: datetime, valid_until: datetime,
                    is_active: bool, min_purchase_amount: decimal, amount: decimal, percent: int,
                    admin_user: BaseUser, usage_number: int) -> Discount:
    discount = Discount.objects.create(
        name=name,
        type=type,
        value_type=value_type,
        valid_from=valid_from,
        valid_until=valid_until,
        is_active=is_active,
        min_purchase_amount=min_purchase_amount,
        amount=amount,
        percent=percent,
        admin_user=admin_user,
        usage_number=usage_number
    )
    discount.code = generate_code(str(discount.id))
    discount.save()
    return discount


def update_discount(*, discount_id: int, name: str, type: int, value_type: int, valid_from: datetime,
                    valid_until: datetime,
                    is_active: bool, min_purchase_amount: decimal, amount: decimal, percent: int,
                    admin_user: BaseUser, usage_number: int) -> Discount:
    discount = Discount.objects.filter(id=discount_id).update(
        name=name,
        type=type,
        value_type=value_type,
        valid_from=valid_from,
        valid_until=valid_until,
        is_active=is_active,
        min_purchase_amount=min_purchase_amount,
        amount=amount,
        percent=percent,
        admin_user=admin_user,
        usage_number=usage_number
    )
    return discount


def delete_discount(*, discount_id: int) -> None:
    Discount.objects.get(id=discount_id).delete()


