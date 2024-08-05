from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cheatgame.api.mixins import ApiAuthMixin
from cheatgame.product.models import SuggestionProduct, Product
from cheatgame.product.permissions import AdminOrManagerPermission
from cheatgame.product.services.suggestion import create_suggestion_product, update_suggestion_product, \
    delete_suggestion_product


class SuggestionProductAdminApi(ApiAuthMixin, APIView):
    permission_classes = (AdminOrManagerPermission,)

    class SuggestionProuductInPutSerializer(serializers.Serializer):
        product = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())
        suggested = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())

    class SuggestionProductOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = SuggestionProduct
            fields = ("id", "product", "suggested")

    @extend_schema(request=SuggestionProuductInPutSerializer, responses=SuggestionProductOutPutSerializer)
    def post(self, request):
        serializer = self.SuggestionProuductInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            suggestion_product = create_suggestion_product(
                product=serializer.validated_data.get("product"),
                suggested=serializer.validated_data.get("suggested")
            )
            return Response(self.SuggestionProductOutPutSerializer(suggestion_product).data,
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class SuggestionProductDetailApi(ApiAuthMixin, APIView):
    permission_classes = (AdminOrManagerPermission,)

    class SuggestionProuductDetailInPutSerializer(serializers.Serializer):
        suggested = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())

    class SuggestionProductDetailOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = SuggestionProduct
            fields = ("id", "product", "suggested")

    @extend_schema(request=SuggestionProuductDetailInPutSerializer, responses=SuggestionProductDetailOutPutSerializer)
    def put(self, request, id: int):
        serializer = self.SuggestionProuductDetailInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            suggestion_product = update_suggestion_product(
                suggestion_id=id,
                suggested=serializer.validated_data.get("suggested"),
            )
            return Response(self.SuggestionProductDetailOutPutSerializer(suggestion_product).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK:dict})
    def delete(self, request, id: int):
        try:
            delete_suggestion_product(suggestion_id=id)
            return Response({"محصول پیشنهادی مورد نظر حذف گردید."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)
