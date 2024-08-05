from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cheatgame.api.mixins import ApiAuthMixin
from cheatgame.product.models import DeliveryOption
from cheatgame.product.permissions import ManagerPermission, AdminOrManagerPermission
from cheatgame.shop.models import DeliverySide, DeliveryType
from cheatgame.shop.selectors.delivery_type import delivery_type_list
from cheatgame.shop.services.delivery_type import create_delivery_type, update_delivery_type, delete_delivery_type


class DeliveryTypeAdminApi(ApiAuthMixin, APIView):
    permission_classes = (AdminOrManagerPermission,)

    class DeliveryTypeInPutSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        delivery_type = serializers.ChoiceField(choices=DeliveryOption.choices())
        side = serializers.ChoiceField(choices=DeliverySide.choices())

    class DeliveryTypeOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = DeliveryType
            fields = ("id", "name", "delivery_type", "side")

    @extend_schema(request=DeliveryTypeInPutSerializer, responses=DeliveryTypeOutPutSerializer)
    def post(self, request):
        serializer = self.DeliveryTypeInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            delivery_type = create_delivery_type(
                name=serializer.validated_data.get("name"),
                delivery_type=serializer.validated_data.get("delivery_type"),
                side=serializer.validated_data.get("side")
            )
            return Response(self.DeliveryTypeOutPutSerializer(delivery_type).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "خطایی رخ داده است"}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryTypeDetailApi(ApiAuthMixin, APIView):
    permission_classes = (AdminOrManagerPermission,)

    class DeliveryTypeDetailInPutSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        delivery_type = serializers.ChoiceField(choices=DeliveryOption.choices())
        side = serializers.ChoiceField(choices=DeliverySide.choices())

    class DeliveryTypeDetailOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = DeliveryType
            fields = ("id", "name", "delivery_type", "side")

    @extend_schema(request=DeliveryTypeDetailInPutSerializer, responses=DeliveryTypeDetailOutPutSerializer)
    def put(self, request, id):
        serializer = self.DeliveryTypeDetailInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            delivery_type_object = update_delivery_type(
                name=serializer.validated_data.get("name"),
                delivery_type=serializer.validated_data.get("delivery_type"),
                side=serializer.validated_data.get("side"),
                delivery_type_id=id
            )
            return Response(self.DeliveryTypeDetailOutPutSerializer(delivery_type_object).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": " خطایی رخ داده است "}, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(responses={status.HTTP_200_OK:dict})
    def delete(self, request, id: int):
        try:
            delete_delivery_type(delivery_type_id=id)
            return Response({"message": "آیتم با موفقیت حذف گردید"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "خطایی رخ داده است"}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryTypeListApi(APIView):
    class DeliveryTypeListOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = DeliveryType
            fields = ("id", "name", "delivery_type", "side")

    @extend_schema(responses=DeliveryTypeListOutPutSerializer)
    def get(self, request):
        try:
            delivery_type_list_objects = delivery_type_list()
            return Response(self.DeliveryTypeListOutPutSerializer(delivery_type_list_objects, many=True).data,
                            status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "خطایی رخ داده است"})
