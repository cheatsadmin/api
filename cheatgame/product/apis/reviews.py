from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cheatgame.api.mixins import ApiAuthMixin
from cheatgame.product.models import RatingChoices, Reviews, Product
from cheatgame.product.permissions import CustomerPermission
from cheatgame.product.services.reviews import create_review
from cheatgame.shop.selectors.cart import bought_order_item


class ReviewsCreateAPIView(ApiAuthMixin , APIView):
    permission_classes = [CustomerPermission , ]


    class ReviewsInPutSerializer(serializers.Serializer):
        product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
        comment = serializers.CharField(required=False)
        rating = serializers.ChoiceField(RatingChoices.choices())

    class ReviewsOutPutSerializer(serializers.ModelSerializer):

        class Meta:
            model = Reviews
            fields = ("user" , "product" , "comment" , "rating")

    @extend_schema(request=ReviewsInPutSerializer , responses= ReviewsOutPutSerializer)
    def post(self , request):
        serializer = self.ReviewsInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        rating = serializer.validated_data.get("rating")
        comment = serializer.validated_data.get("comment" , None)
        product = serializer.validated_data.get("product")
        user = request.user
        if not bought_order_item(user=user , product_id=product.id):
            return Response({"error": "کاربر برای ثبت نظر باید قبلا این محصول را خریداری کرده باشید."}, status=status.HTTP_400_BAD_REQUEST)
        review = create_review(user = user , product = product ,rating=rating , comment=comment)
        return Response(self.ReviewsOutPutSerializer(review).data , status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error": "مشکلی در ثبت نظر شما پیش آمده است."} , status=status.HTTP_400_BAD_REQUEST)


