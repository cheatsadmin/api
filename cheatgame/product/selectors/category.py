from django.db.models import QuerySet

from cheatgame.product.models import Category


def get_category_list(*, category_type: int) -> QuerySet[Category]:
    return Category.objects.filter(category_type=category_type, parent__isnull=True)


def get_all_categories() -> QuerySet[Category]:
    return Category.objects.all()
