from django.db.models import QuerySet

from cheatgame.product.filters import QuestionFilter
from cheatgame.product.models import Question


def question_list(*, filters=None) -> QuerySet[Question]:
    filters = filters or {}
    qs = Question.objects.all()
    return QuestionFilter(filters, qs).qs