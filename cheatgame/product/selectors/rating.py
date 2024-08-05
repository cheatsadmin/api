from django.db.models import QuerySet

from cheatgame.product.filters import ReviewFilter
from cheatgame.product.models import Reviews


def review_list(*, filters=None) -> QuerySet[Reviews]:
    filters = filters or {}
    qs = Reviews.objects.all()
    return ReviewFilter(filters, qs).qs