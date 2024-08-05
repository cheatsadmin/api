from datetime import datetime
import decimal

from django.db.models import QuerySet

from cheatgame.shop.models import Discount, UserDiscount, DiscountType
from cheatgame.users.models import BaseUser
from cheatgame.users.selectors import user_address_list


def discount_list_admin() -> QuerySet[Discount]:
    return Discount.objects.filter(is_active=True).order_by("-id")


def discount_list_user(*, user: BaseUser) -> QuerySet[UserDiscount]:
    now = datetime.now()
    return UserDiscount.objects.filter(user=user, discount__valid_from__lt=now, discount__valid_until__gt=now,
                                       discount__is_active=True , discount__type = DiscountType.DIRECT , is_used = False)


def check_discount_code(*, code: str, total_price: decimal, user: BaseUser) -> bool:
    now = datetime.now()
    discount = Discount.objects.get(valid_from__lt=now, valid_until__gt=now, code=code)
    if discount:
        user_discount = UserDiscount.objects.filter(discount=discount, user=user)
        if not user_discount.first():
            return False
        return discount.min_purchase_amount <= total_price and not user_discount.first().is_used
    return False


def check_coupon_code(*, code: str, total_price: decimal) -> bool:
    now = datetime.now()
    discount = Discount.objects.get(valid_from__lt=now, valid_until__gt=now, code=code)
    if discount:
        return discount.min_purchase_amount <= total_price and discount.usage_number > 0
    return False
