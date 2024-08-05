import decimal
from decimal import Decimal

from cheatgame.product.models import Product, Reviews
from cheatgame.users.models import BaseUser
from django.db.models import Avg , F

def create_review(*, user: BaseUser, product: Product, rating: int, comment: str) -> Reviews:
    review = Reviews.objects.create(user=user, product=product, rating=rating, comment=comment)
    calculate_product_ranting(product= product)
    return review

def calculate_product_ranting(* ,product: Product) -> None:
    review= Reviews.objects.filter(product=product).aggregate(average_ranting = Avg('rating'))
    rating_avg = review.get("average_ranting")
    product.score = Decimal(rating_avg)
    product.save(update_fields=["score" , "updated_at"])

