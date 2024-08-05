import datetime

from django.db import transaction
from django.utils.text import slugify

from cheatgame.product.models import Product, ProductNote


@transaction.atomic
def create_product(*, product_type: int, title: str, main_image: str, price: float, off_price: float,
                   quantity: int, discount_end_time: datetime = None, description: str, included_products: list = None,
                   order_limit: int = None, device_model: str) -> Product:
    product = Product.objects.create(
        product_type=product_type,
        title=title,
        slug=slugify(title, allow_unicode=True),
        main_image=main_image,
        price=price,
        off_price=off_price,
        quantity=quantity,
        discount_end_time=discount_end_time,
        description=description,
        order_limit=order_limit,
        device_model=device_model,
    )
    if included_products:
        product_ids = [product.id for product in included_products]
        included_products = Product.objects.filter(id__in=product_ids)
        product.included_products.add(*included_products)
    return product


def check_product_exists(*, product_id: int) -> bool:
    return Product.objects.filter(id=product_id).exists()

def delete_product(*, product_id: int) -> None:
    Product.objects.filter(id=product_id).delete()

def update_product(*, product_id: int, product_type: int, title: str, main_image: str = None, price: float, off_price: float,
                   quantity: int, discount_end_time: datetime = None, description: str =None,
                   order_limit: int = None, device_model: str) -> Product:
    product = Product.objects.select_for_update().get(id=product_id)
    product.product_type = product_type
    product.title = title
    if main_image is not None:
        product.main_image = main_image
    product.price = price
    product.off_price = off_price
    product.quantity = quantity
    product.discount_end_time = discount_end_time
    if description is not None:
        product.description = description
    product.order_limit = order_limit
    product.device_model = device_model
    product.save(
        update_fields=["product_type", "title", "main_image", "price", "off_price", "quantity", "discount_end_time",
                       "description", "order_limit", "device_model" ,"updated_at"])
    return product


def create_product_note(*, product: Product, title: str) -> ProductNote:
    return ProductNote.objects.create(
        product=product,
        title=title
    )


def update_product_note(*, product_note_id: int, title: str, product: Product) -> ProductNote:
    product_note = ProductNote.objects.get(id=product_note_id)
    product_note.product = product
    product_note.title = title
    product_note.save()
    return product_note


def delete_product_note(*, product_note_id: int) -> None:
    ProductNote.objects.get(id=product_note_id).delete()
