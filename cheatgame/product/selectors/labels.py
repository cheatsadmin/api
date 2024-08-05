from django.db.models import QuerySet

from cheatgame.product.models import Label


def get_all_labels() ->QuerySet[Label]:
    return Label.objects.all()