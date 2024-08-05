from cheatgame.product.models import Label, Product, ProductLabel


def create_label(*, label_type: int, name: str) -> Label:
    return Label.objects.create(
        label_type=label_type,
        name=name
    )


def update_label(*, label_id: int, label_type: int, name: str) -> Label:
    label = Label.objects.get(id=label_id)
    label.label_type = label_type
    label.name = name
    label.save()
    return label


def delete_label(*, label_id=int) -> None:
    Label.objects.get(id=label_id).delete()


def create_product_label(*, label: Label, product: Product) -> ProductLabel:
    return ProductLabel.objects.create(
        label=label,
        product=product
    )


def update_product_label(*, product_label_id: int, label: Label, product: Product) -> ProductLabel:
    product_label = ProductLabel.objects.get(id=product_label_id)
    product_label.label = label
    product_label.product = product
    product_label.save()
    return product_label


def delete_product_label(*, product_label_id: int) -> None:
    ProductLabel.objects.get(id=product_label_id).delete()
