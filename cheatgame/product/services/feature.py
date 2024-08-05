from cheatgame.product.models import Category, Feature, Product, ValuesList


def create_feature(*, name: str, feature_type: int, category: Category) -> Feature:
    return Feature.objects.create(
        name=name,
        feature_type=feature_type,
        category=category
    )


def create_product_feature(*, value: str, product: Product, feature: Feature) -> ValuesList:
    return ValuesList.objects.create(
        value=value,
        product=product,
        feature=feature
    )


def update_feature(*, feature_id: int, name: str, feature_type: int, category: Category) -> Feature:
    feature = Feature.objects.get(id=feature_id)
    feature.name = name
    feature.feature_type = feature_type
    feature.category = category
    feature.save()
    return feature


def delete_feature(*, feature_id: int) -> None:
    Feature.objects.get(id=feature_id).delete()


def update_product_feature(*, product_feature_id: int, value: str, product: Product, feature: Feature) -> ValuesList:
    values_list = ValuesList.objects.get(id=product_feature_id)
    values_list.value = value
    values_list.product = product
    values_list.feature = feature
    values_list.save()
    return values_list


def delete_product_feature(*, product_feature_id) -> None:
    ValuesList.objects.get(id=product_feature_id).delete()
