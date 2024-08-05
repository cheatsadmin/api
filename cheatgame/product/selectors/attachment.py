from django.db.models import QuerySet

from cheatgame.product.models import Attachment


def get_attachment(*, attachement_id: int) -> Attachment:
    return Attachment.objects.get(id=attachement_id)


def attachment_list_product(*, product_id: int) -> QuerySet[Attachment]:
    return Attachment.objects.filter(product_id=product_id)
