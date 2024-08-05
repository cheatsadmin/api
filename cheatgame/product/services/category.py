from django.db.models import QuerySet

from cheatgame.product.models import Category, ProductCategory, Product
from django.utils.text import slugify


def create_category(*, name: str, category_type: int, parent: Category) -> Category:
    return Category.objects.create(
        name=name,
        slug=slugify(name, allow_unicode=True),
        category_type=category_type,
        parent=parent
    )


def update_category(*, category_id: int, name: str, category_type: int, parent: Category) -> Category:
    category = Category.objects.get(id=category_id)
    category.name = name
    category.category_type = category_type
    category.parent = parent
    category.slug = slugify(name, allow_unicode=True)
    category.save()
    return category


def delete_category(category_id: int) -> None:
    Category.objects.get(id=category_id).delete()


def create_product_categories(*, product_category: list[ProductCategory]) -> QuerySet[ProductCategory]:
    return ProductCategory.objects.bulk_create(product_category)


def update_product_category(*, product_category_id: int, product: Product, category: Category) -> ProductCategory:
    product_category = ProductCategory.objects.get(id=product_category_id)
    product_category.product = product
    product_category.category = category
    product_category.save()
    return product_category


def delete_product_category(*, product_category_id) -> None:
    ProductCategory.objects.get(id=product_category_id).delete()
