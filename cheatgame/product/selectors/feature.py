from cheatgame.product.models import Feature


def get_all_features():
    return Feature.objects.all()