import decimal
from _decimal import Decimal
from typing import List
from unicodedata import decimal

from django.db import transaction
from django.utils import timezone

from cheatgame.product.models import Product, Attachment, ProductType
from cheatgame.shop.models import Cart, CartItemAttachment, CartItem, OrderItemAttachment, OrderItem
from cheatgame.users.models import BaseUser


def check_product_limit(*, product: Product, quantity: int) -> bool:
    return product.order_limit >= quantity


def check_product_avaliablity(*, product: Product, quantity: int) -> bool:
    if product.quantity <= 0:
        return False
    return product.quantity - quantity >= 0


def get_cart_or_create(*, user: BaseUser) -> Cart:
    cart = Cart.objects.filter(user=user)
    if cart:
        return cart.first()
    return Cart.objects.create(user=user)


def check_attachment(*, attachments: List[Attachment], ) -> bool:
    attachment_type_list = []
    # TODO: also check force attachments
    for item in attachments:
        attachment = item["attachment"]
        print(attachment)
        if attachment.attachment_type in attachment_type_list:
            return False
        else:
            attachment_type_list.append(attachment.attachment_type)
    return True


def check_attachment_order(*, attachments: List[Attachment]) -> bool:
    attachment_type_list = []
    for attachment in attachments:
        if attachment.attachment_type in attachment_type_list:
            return False
        else:
            attachment_type_list.append(attachment.attachment_type)
    return True


def calculate_attchment_price_cart(*, attachments: List[Attachment], product: Product, cart_item: CartItem) -> decimal:
    total_price = Decimal("0.0")
    cart_item_attachment = []

    if attachments:
        for item in attachments:
            attachment = item["attachment"]
            if product.product_type == ProductType.GAME:
                total_price = attachment.price
            else:
                total_price += attachment.price
            cart_item_attachment.append(CartItemAttachment(cart_item=cart_item, attachment=attachment))
        CartItemAttachment.objects.bulk_create(cart_item_attachment)
        return total_price
    else:
        attachments_objects = Attachment.objects.filter(product=product, is_force_attachement=True)
        for item in attachments_objects:
            attachment = item["attachment"]
            if product.product_type == ProductType.GAME:
                total_price = attachment.price
            else:
                total_price += attachment.price
            cart_item_attachment.append(CartItemAttachment(cart_item=cart_item, attachment=attachment))
        CartItemAttachment.objects.bulk_create(cart_item_attachment)
        return total_price


def calculate_attchment_price_order(*, attachments: List[Attachment], product: Product,
                                    order_item: OrderItem) -> decimal:
    total_price = Decimal("0.0")
    order_item_attachment = []

    if attachments:
        for attachment in attachments:
            if product.product_type == ProductType.GAME:
                total_price = attachment.price
            else:
                total_price += attachment.price
            print(f"{type(order_item)}=")
            print(f'{type(attachment)}=')
            print("print if ")
            order_item_attachment.append(OrderItemAttachment(order_item=order_item, attachment=attachment))
        OrderItemAttachment.objects.bulk_create(order_item_attachment)
        return total_price
    else:
        attachments_objects = Attachment.objects.filter(product=product, is_force_attachement=True)
        for attachment in attachments_objects:
            if product.product_type == ProductType.GAME:
                total_price = attachment.price
            else:
                total_price += attachment.price
            print("else if print")
            print(f"{type(order_item)}=")
            print(f'{type(attachment)}=')
            order_item_attachment.append(OrderItemAttachment(order_item=order_item, attachment=attachment))
        OrderItemAttachment.objects.bulk_create(order_item_attachment)
        return total_price


def check_cart_item_exists(*, product: Product, user: BaseUser) -> bool:
    if CartItem.objects.filter(product=product, cart__user=user).exists():
        return True
    return False


@transaction.atomic
def add_to_cart(*, attachment: List[Attachment], quantity: int, product: Product, user: BaseUser) -> CartItem:
    cart = get_cart_or_create(user=user)
    cart_item = CartItem.objects.create(cart=cart, price=0, product=product)
    total_attachment_price = calculate_attchment_price_cart(attachments=attachment, cart_item=cart_item,
                                                            product=product)
    cart_item.quantity = quantity
    price = product.price if not product.discount_end_time or product.discount_end_time < timezone.now() else product.off_price
    if product.product_type == ProductType.GAME:
        cart_item.price = total_attachment_price * quantity
    else:
        cart_item.price = price * quantity + total_attachment_price
    cart_item.save()
    return cart_item


def cartitem_attachment_total_price(*, cart_item: CartItem) -> decimal:
    attachment_list = CartItemAttachment.objects.filter(cart_item=cart_item)
    total_price = 0
    for attachment in attachment_list:
        if cart_item.product.product_type == ProductType.GAME:
            total_price = attachment.attachment.price
        else:
            total_price += attachment.attachment.price
    return total_price


@transaction.atomic
def update_cart_item(*, cart_item: CartItem, quantity: int = None):
    price = cart_item.product.price if not cart_item.product.discount_end_time or cart_item.product.discount_end_time < timezone.now() else cart_item.product.off_price
    attachment_price = cartitem_attachment_total_price(cart_item=cart_item)
    if cart_item.product.product_type == ProductType.GAME:
        cart_item.price = quantity * attachment_price
    else:
        cart_item.price = quantity * price + attachment_price
    cart_item.quantity = quantity
    cart_item.save()
    return cart_item


def delete_cart_item(*, cart_item_id: int) -> None:
    CartItem.objects.get(id=cart_item_id).delete()
