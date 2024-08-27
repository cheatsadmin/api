from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from cheatgame.api.mixins import ApiAuthMixin
from cheatgame.api.pagination import LimitOffsetPagination, get_paginated_response, PaginatedSerializer, get_paginated_response_context
from cheatgame.api.utils import inline_serializer
from cheatgame.common.utils import reformat_url
from cheatgame.product.models import ProductType, Product, ProductOrderBy, Image, Category, Feature, ValuesList, \
    Attachment, Question, Label, ProductNote
from cheatgame.product.permissions import AdminOrManagerPermission
from cheatgame.product.selectors.product import product_list, product_detail, product_list_by_slug
from cheatgame.product.services.product import create_product, create_product_note, update_product_note, \
    delete_product_note, update_product, check_product_exists, delete_product
from cheatgame.users.models import BaseUser


class ProductDetailProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    def get_main_image(self, obj):
        return reformat_url(url=obj.main_image.url)

    class Meta:
        model = Product
        fields = ("id", "product_type", "title", "slug", "main_image", "price", "off_price", "quantity", "device_model")


class ProductAdminApi(ApiAuthMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = (AdminOrManagerPermission,)

    class ProductCreateInputSerializer(serializers.Serializer):
        product_type = serializers.ChoiceField(choices=ProductType.choices())
        title = serializers.CharField(max_length=100)
        main_image = serializers.FileField(required=True)
        price = serializers.DecimalField(max_digits=15, decimal_places=0)
        off_price = serializers.DecimalField(max_digits=15, decimal_places=0)
        quantity = serializers.IntegerField(required=True)
        discount_end_time = serializers.DateTimeField(required=False)
        description = serializers.FileField()
        order_limit = serializers.IntegerField(required=False)
        device_model = serializers.CharField(max_length=100, required=False, allow_blank=True)
        included_products = serializers.PrimaryKeyRelatedField(required=False, many=True,
                                                               queryset=Product.objects.filter(
                                                                   product_type=ProductType.GAME))

        def validate_included_products(self, included_products):
            if len(included_products) > 5:
                raise serializers.ValidationError("حداکثر تعداد محصول مجاز ۵ عدد می باشد.")
            return included_products

    class ProuductCreateOutputSerializer(serializers.ModelSerializer):
        main_image = serializers.SerializerMethodField()
        description = serializers.SerializerMethodField()

        def get_main_image(self, obj):
            return reformat_url(url=obj.main_image.url)

        def get_description(self, obj):
            return reformat_url(url=obj.description.url)

        class Meta:
            model = Product
            fields = ("id", "product_type", "title", "slug", "main_image",
                      "price", "off_price", "quantity", "discount_end_time",
                      "description", "included_products", "order_limit",
                      "device_model", "created_at", "updated_at")

    @extend_schema(request=ProductCreateInputSerializer,
                   responses={status.HTTP_201_CREATED: ProuductCreateOutputSerializer})
    def post(self, request):
        serializer = self.ProductCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = create_product(
                product_type=serializer.validated_data.get("product_type"),
                title=serializer.validated_data.get("title"),
                main_image=request.FILES.get("main_image"),
                price=serializer.validated_data.get("price"),
                off_price=serializer.validated_data.get("off_price"),
                quantity=serializer.validated_data.get("quantity"),
                discount_end_time=serializer.validated_data.get("discount_end_time", None),
                description=serializer.validated_data.get("description"),
                included_products=serializer.validated_data.get("included_products", None),
                order_limit=serializer.validated_data.get("order_limit", None),
                device_model=serializer.validated_data.get("device_model", None)
            )
            return Response(self.ProuductCreateOutputSerializer(product).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAdminApi(ApiAuthMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AdminOrManagerPermission, ]

    class ProductDetailInPutSerializer(serializers.Serializer):
        product_type = serializers.ChoiceField(choices=ProductType.choices())
        title = serializers.CharField(max_length=100)
        main_image = serializers.FileField(required=True)
        price = serializers.DecimalField(max_digits=15, decimal_places=0)
        off_price = serializers.DecimalField(max_digits=15, decimal_places=0)
        quantity = serializers.IntegerField(required=True)
        discount_end_time = serializers.DateTimeField(required=False)
        description = serializers.FileField()
        order_limit = serializers.IntegerField(required=False)
        device_model = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class ProductDetailOutPutSerializer(serializers.ModelSerializer):
        main_image = serializers.SerializerMethodField()
        description = serializers.SerializerMethodField()

        def get_main_image(self, obj):
            return reformat_url(url=obj.main_image.url)

        def get_description(self, obj):
            return reformat_url(url=obj.description.url)

        class Meta:
            model = Product
            fields = (
                "id", "product_type", "title", "main_image", "price", "off_price", "quantity", "discount_end_time",
                "description", "order_limit", "device_model")

    @extend_schema(request=ProductDetailInPutSerializer, responses={200: ProductDetailOutPutSerializer})
    def put(self, request, id):
        serializer = self.ProductDetailInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        if not check_product_exists(product_id=id):
            return Response({"error": "محصول موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
        main_image = request.FILES.get("main_image", None)
        description = request.FILES.get("description", None)
        product = update_product(
            product_id=id,
            product_type=serializer.validated_data.get("product_type"),
            title=serializer.validated_data.get("title"),
            main_image=main_image,
            price=serializer.validated_data.get("price"),
            off_price=serializer.validated_data.get("off_price"),
            quantity=serializer.validated_data.get("quantity"),
            discount_end_time=serializer.validated_data.get("discount_end_time"),
            description=description,
            order_limit=serializer.validated_data.get("order_limit"),
            device_model=serializer.validated_data.get("device_model")
        )
        return Response(self.ProductDetailOutPutSerializer(product).data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error": "مشکلی در آپدیت محصول به وجود آمده است."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK: dict})
    def delete(self, request, id):
        try:
            if not check_product_exists(product_id=id):
                return Response({"error": "محصول موجود نیست"}, status=status.HTTP_400_BAD_REQUEST)
            delete_product(product_id=id)
            return Response({"message": "محصول مورد نظر حذف گردید."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "مشکلی در حذف محصول به وجود آمده است."}, status=status.HTTP_400_BAD_REQUEST)


class ProudctOutPutSerializer(serializers.ModelSerializer):
    included_products = ProductDetailProductSerializer(many=True)
    main_image = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()

    def get_category_id(self, obj):
        global category_slug
        request = self.context.get('request', None)
        if request:
            category_slug = request.parser_context["kwargs"]["slug"]
        category_object = Category.objects.get(slug=category_slug)
        return category_object.id

    def get_main_image(self, obj):
        return reformat_url(url=obj.main_image.url)

    attachments = inline_serializer(many=True,
                                    fields={
                                        "id": serializers.CharField(required=False),
                                        "title": serializers.CharField(required=False),
                                        "attachment_type": serializers.IntegerField(required=False),
                                        "price": serializers.DecimalField(max_digits=15, decimal_places=0,
                                                                          required=False),
                                        "is_force_attachment": serializers.BooleanField(required=False),
                                        "description" : serializers.CharField(required=False , max_length=250)
                                    })

    class Meta:
        model = Product
        fields = ("id", "product_type", "title", "slug", "main_image",
                  "price", "off_price", "discount_end_time",
                  "included_products", "order_limit", "device_model", "attachments" , "score",
                  "category_id",
                  )


class ProudctApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterProductSerializer(serializers.Serializer):
        product_type = serializers.ChoiceField(required=False, choices=ProductType.choices())
        search = serializers.CharField(required=False, max_length=100)
        off_price__range = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        has_discount = serializers.CharField(required=False)
        categories__in = serializers.CharField(required=False, max_length=200)
        labels__in = serializers.CharField(required=False, max_length=100)
        is_exists = serializers.CharField(required=False)
        order_by = serializers.ChoiceField(required=False, choices=ProductOrderBy.choices())

    class PaginatedProductSerializer(PaginatedSerializer):
        results = ProudctOutPutSerializer(many=True)

    class PaginationParameterSerializer(serializers.Serializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    @extend_schema(parameters=[FilterProductSerializer, PaginationParameterSerializer],
                   responses=PaginatedProductSerializer, )
    def get(self, request):
        filters_serializer = self.FilterProductSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        try:
            query = product_list(filters=filters_serializer.validated_data)
        except Exception as error:
            return Response(
                {"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=ProudctOutPutSerializer,
            queryset=query,
            view=self,
            request=request
        )


class ProudctApiBySlug(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class PaginatedProductSerializer(PaginatedSerializer):
        results = ProudctOutPutSerializer(many=True)

    class PaginationParameterSerializer(serializers.Serializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)

    @extend_schema(parameters=[PaginationParameterSerializer],
                   responses=PaginatedProductSerializer, )
    def get(self, request, slug: str):
        try:
            query = product_list_by_slug(slug=slug)
        except Exception as error:
            return Response(
                {"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=ProudctOutPutSerializer,
            queryset=query,
            view=self,
            request=request
        )


class ProductDetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class ProductDetailFeatureSerializer(serializers.ModelSerializer):
    category = ProductDetailCategorySerializer(read_only=True)

    class Meta:
        model = Feature
        fields = ("name", "category")


class ProductDetailLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ("name", "label_type",)


class ProductDetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ("firstname", "lastname",)


class ProductDetailApi(APIView):
    class ProductDetailOutPutSerializer(serializers.Serializer):

        comments_count = serializers.SerializerMethodField()

        images = inline_serializer(many=True,
                                   fields={
                                       "id": serializers.CharField(required=False),
                                       "file": serializers.FileField(required=False)
                                   })
        included_products = inline_serializer(many=True,
                                              fields={
                                                  "id": serializers.CharField(required=False),
                                                  "product_type": serializers.IntegerField(required=False),
                                                  "title": serializers.CharField(required=False),
                                                  "main_image": serializers.FileField(required=False),
                                              })
        valueslist = inline_serializer(many=True,
                                       fields={
                                           "id": serializers.CharField(required=False),
                                           "feature": ProductDetailFeatureSerializer(required=False),
                                           "value": serializers.CharField(required=False),
                                       })
        attachments = inline_serializer(many=True,
                                        fields={
                                            "id": serializers.CharField(required=False),
                                            "title": serializers.CharField(required=False),
                                            "attachment_type": serializers.IntegerField(required=False),
                                            "price": serializers.DecimalField(max_digits=15, decimal_places=0,
                                                                              required=False),
                                            "is_force_attachment": serializers.BooleanField(required=False),
                                            "description": serializers.CharField(max_length=250)
                                        })
        suggestions = inline_serializer(many=True, fields={
            "id": serializers.CharField(required=False),
            "suggested": ProductDetailProductSerializer(required=False),
        })
        labels = inline_serializer(many=True, fields={
            "id": serializers.CharField(required=False),
            "label": ProductDetailLabelSerializer(required=False)
        })

        reviews = inline_serializer(many=True, fields={
            "id": serializers.CharField(required=False),
            "user": ProductDetailUserSerializer(required=False),
            "comment": serializers.CharField(required=False),
            "created_at": serializers.DateTimeField(required=False),
        })

        questions = inline_serializer(many=True, fields={
            "id": serializers.CharField(required=False),
            "sender": ProductDetailUserSerializer(required=False),
            "question": serializers.CharField(required=False),
            "answer": serializers.CharField(required=False)
        })

        notes = inline_serializer(many=True, fields={
            "id": serializers.CharField(required=False),
            "title": serializers.CharField(max_length=100),
        })
        product_type = serializers.IntegerField()
        title = serializers.CharField()
        slug = serializers.SlugField()
        main_image = serializers.SerializerMethodField()
        price = serializers.DecimalField(decimal_places=0, max_digits=15)
        off_price = serializers.DecimalField(decimal_places=0, max_digits=15)
        quantity = serializers.IntegerField()
        device_model = serializers.CharField()
        id = serializers.IntegerField()
        description = serializers.FileField()
        discount_end_time = serializers.DateTimeField()
        score = serializers.DecimalField(decimal_places=1, max_digits=4)
        created_at = serializers.DateTimeField(required=False)
        updated_at = serializers.DateTimeField(required=False)
        def to_representation(self, instance):
            representation = super().to_representation(instance)
            images_data = representation["images"]
            included_products_data = representation["included_products"]
            print(f"{images_data=}")
            for image_data in images_data:
                image_data["file"] = reformat_url(url =image_data["file"])

            for included_product in included_products_data:
                included_product["main_image"] = reformat_url(url = included_product["main_image"])
            representation["included_products"] = included_products_data
            representation["images"] = images_data
            return representation



        def get_comments_count(self, product: Product) -> int:
            return Question.objects.filter(accepted=True, product=product).count()

        def get_main_image(self , obj):
            return reformat_url(url = obj.main_image.url)

        def get_description(self , obj):
            return reformat_url(url = obj.description.url)
        
        
        

    @extend_schema(responses=ProductDetailOutPutSerializer)
    def get(self, request, slug: str):
        try:
            product = product_detail(
                slug=slug
            )
            serializer = self.ProductDetailOutPutSerializer(instance=product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class ProductNoteAdminApi(ApiAuthMixin, APIView):
    permission_classes = (AdminOrManagerPermission,)

    class ProductNoteInPutSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class ProductNoteOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductNote
            fields = ("id", "title", "product")

    @extend_schema(request=ProductNoteInPutSerializer, responses=ProductNoteOutPutSerializer)
    def post(self, request):
        serializer = self.ProductNoteInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product_note = create_product_note(
                title=serializer.validated_data.get("title"),
                product=serializer.validated_data.get("product")
            )
            return Response(self.ProductNoteOutPutSerializer(product_note).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class ProductNoteDetailApi(ApiAuthMixin, APIView):
    class ProductNoteDetailInPutSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class ProductNoteDetailOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductNote
            fields = ("id", "title", "product")

    @extend_schema(request=ProductNoteDetailInPutSerializer, responses=ProductNoteDetailOutPutSerializer)
    def put(self, request, id: int):
        serializer = self.ProductNoteDetailInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product_note = update_product_note(
                product_note_id=id,
                title=serializer.validated_data.get("title"),
                product=serializer.validated_data.get("product")
            )
            return Response(self.ProductNoteDetailOutPutSerializer(product_note).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK: dict})
    def delete(self, request, id: int):
        try:
            delete_product_note(product_note_id=id)
            return Response({"message": "آیتم مورد نظر حذف گردید"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)
