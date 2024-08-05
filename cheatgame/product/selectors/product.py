from django.db.models import QuerySet, Prefetch

from cheatgame.product.filters import ProductFilter
from cheatgame.product.models import Product, Question, Reviews, Label, LabelType, SuggestionProduct


def product_list(*, filters=None) -> QuerySet[Product]:
    filters = filters or {}
    qs = Product.objects.all()
    return ProductFilter(filters, qs).qs.prefetch_related("attachments")


def products_numbers() -> int:
    return Product.objects.all().count()


def product_detail(*, slug: str) -> Product:
    return Product.objects.filter(slug=slug).prefetch_related(
        "images",
        "categories",
        "valueslist",
        "attachments",
        "suggestions",
        "labels",
        Prefetch("reviews", queryset=Reviews.objects.filter(accepted=True)),
        Prefetch("questions", queryset=Question.objects.filter(accepted=True)),
        "notes"
    ).first()


def label_list_brands() -> QuerySet[Label]:
    return Label.objects.filter(label_type=LabelType.BRAND)

def label_list_consoles() -> QuerySet[Label]:
    return Label.objects.filter(label_type=LabelType.CONSOLE)

def label_list_capabilities() -> QuerySet[Label]:
    return Label.objects.filter(label_type=LabelType.CAPACITY)


def suggestions_product(*, product: Product):
    suggestion_objects = SuggestionProduct.objects.filter(product=product).select_related("suggested")
    suggested_list = [instance.suggested for instance in suggestion_objects ]
    return suggested_list


