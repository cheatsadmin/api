from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cheatgame.api.mixins import ApiAuthMixin
from cheatgame.product.models import LabelType, Label, ProductLabel, Product
from cheatgame.product.permissions import AdminOrManagerPermission
from cheatgame.product.selectors.labels import get_all_labels
from cheatgame.product.selectors.product import label_list_brands, label_list_capabilities, label_list_consoles
from cheatgame.product.services.label import create_label, create_product_label, update_label, delete_label, \
    update_product_label, delete_product_label


class LabelAdminApi(ApiAuthMixin, APIView):
    class LabelInPutSerializer(serializers.Serializer):
        label_type = serializers.ChoiceField(choices=LabelType.choices())
        name = serializers.CharField(max_length=100)

    class LabelOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Label
            fields = ("id", "label_type", "name")



    @extend_schema(request=LabelInPutSerializer, responses={status.HTTP_201_CREATED:LabelOutPutSerializer})
    def post(self, request):
        serializer = self.LabelInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            label = create_label(
                label_type=serializer.validated_data.get("label_type"),
                name=serializer.validated_data.get("name")
            )
            return Response(self.LabelOutPutSerializer(label).data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class LabelListAdminApi(ApiAuthMixin ,APIView):

    permission_classes = [AdminOrManagerPermission ,]
    class LabelListOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Label
            fields = "__all__"


    @extend_schema(responses=LabelListOutPutSerializer(many=True))
    def get(self, request, *args, **kwargs):
        try:
            labels = get_all_labels()
            return Response(self.LabelListOutPutSerializer(labels , many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی در گرفتن لیست پیش آمده است"} , status=status.HTTP_400_BAD_REQUEST)

class LabelDetailAdminApi(ApiAuthMixin, APIView):
    class LabelDetailInPutSerializer(serializers.Serializer):
        label_type = serializers.ChoiceField(choices=LabelType.choices())
        name = serializers.CharField(max_length=100)

    class LabelDetailOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Label
            fields = ("id", "label_type", "name")

    @extend_schema(request=LabelDetailInPutSerializer, responses={status.HTTP_200_OK:LabelDetailOutPutSerializer})
    def put(self, request, id):
        serializer = self.LabelDetailInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            label = update_label(
                label_id=id,
                label_type=serializer.validated_data.get("label_type"),
                name=serializer.validated_data.get("name")
            )
            return Response(self.LabelDetailOutPutSerializer(label).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK:dict})
    def delete(self, request, id: int):
        try:
            delete_label(label_id=id)
            return Response({"message": "لیبل با موفقیت حذف گردید."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class ProductLabelAdminApi(ApiAuthMixin, APIView):
    class ProductLabelInPutSerializer(serializers.Serializer):
        label = serializers.PrimaryKeyRelatedField(required=True, queryset=Label.objects.all())
        product = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())

    class ProductLabelOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductLabel
            fields = ("id", "label", "product")

    @extend_schema(request=ProductLabelInPutSerializer, responses=ProductLabelOutPutSerializer)
    def post(self, request):
        serializer = self.ProductLabelInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product_label = create_product_label(
                label=serializer.validated_data.get("label"),
                product=serializer.validated_data.get("product")

            )
            return Response(self.ProductLabelOutPutSerializer(product_label).data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class ProductLabelDetailAdminApi(ApiAuthMixin, APIView):
    class ProductLabelDetailInPutSerializer(serializers.Serializer):
        label = serializers.PrimaryKeyRelatedField(required=True, queryset=Label.objects.all())
        product = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())

    class ProductLabelDetailOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductLabel
            fields = ("id", "label", "product")

    @extend_schema(request=ProductLabelDetailInPutSerializer, responses=ProductLabelDetailOutPutSerializer)
    def put(self, request, id: int):
        serializer = self.ProductLabelDetailInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product_label = update_product_label(
                product_label_id=id,
                label=serializer.validated_data.get("label"),
                product=serializer.validated_data.get("product")
            )
            return Response(self.ProductLabelDetailOutPutSerializer(product_label).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK:dict})
    def delete(self, request, id: int):
        try:
            delete_product_label(product_label_id=id)
            return Response({"message": "لیبل محصول با موفقیت حذف گردید."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class LabelListApi(APIView):
    class LabelListOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Label
            fields = ("id", "label_type", "name")

    @extend_schema(responses=LabelListOutPutSerializer)
    def get(self, request):
        try:
            labels = label_list_brands()
            return Response(self.LabelListOutPutSerializer(labels, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "خطایی رخ داده است"}, status=status.HTTP_400_BAD_REQUEST)
class CosoleLabelListApi(LabelListApi):
    class ConsoleLabelListOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Label
            fields = ("id", "label_type", "name")

    @extend_schema(responses=ConsoleLabelListOutPutSerializer)
    def get(self , request):
        try:
            console_list = label_list_consoles()
            return Response(self.ConsoleLabelListOutPutSerializer(console_list, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "خطایی رخ داده است"}, status=status.HTTP_400_BAD_REQUEST)

class CapacityLabelListApi(LabelListApi):
    class CapacityLabelListOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Label
            fields = ("id", "label_type", "name")

    @extend_schema(responses=CapacityLabelListOutPutSerializer)
    def get(self , request):
        try:
            capacity_label_list = label_list_capabilities()
            return Response(self.CapacityLabelListOutPutSerializer(capacity_label_list, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "خطایی رخ داده است"}, status=status.HTTP_400_BAD_REQUEST)
            
        

            
