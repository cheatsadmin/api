from cheatgame.product.models import Product, SuggestionProduct


def create_suggestion_product(*, product: Product, suggested: Product) -> SuggestionProduct:
    return SuggestionProduct.objects.create(
        product=product,
        suggested=suggested
    )


def update_suggestion_product(*, suggestion_id: int, suggested: Product) -> SuggestionProduct:
    suggestion  = SuggestionProduct.objects.get(id = suggestion_id)
    suggestion.suggested = suggested
    suggestion.save()
    return suggestion

def delete_suggestion_product(* , suggestion_id:int) -> None:
    SuggestionProduct.objects.get(id = suggestion_id).delete()

