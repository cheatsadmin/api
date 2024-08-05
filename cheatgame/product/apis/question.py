from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cheatgame.api.mixins import ApiAuthMixin
from cheatgame.api.pagination import PaginatedSerializer, LimitOffsetPagination, get_paginated_response
from cheatgame.product.models import Question, Product
from cheatgame.product.permissions import CustomerPermission, QuestionIsOwnerCustomer, AdminOrManagerPermission
from cheatgame.product.selectors.questions import question_list
from cheatgame.product.services.question import create_question, update_question, delete_question


class QuestionApi(ApiAuthMixin, APIView):
    permission_classes = (CustomerPermission,)

    class QuestionInputSerializer(serializers.Serializer):
        product = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())
        question = serializers.CharField(required=True)

    class QuestionOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ("id", "question", "product")

    @extend_schema(request=QuestionInputSerializer, responses=QuestionOutPutSerializer)
    def post(self, request):
        serializer = self.QuestionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            question = create_question(product=serializer.validated_data.get("product"),
                                       question=serializer.validated_data.get("question"),
                                       sender=request.user)
            return Response(self.QuestionOutPutSerializer(question).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAdminApi(ApiAuthMixin, APIView):
    permission_classes = (CustomerPermission, QuestionIsOwnerCustomer)

    class QuestionDetailInputSerializer(serializers.Serializer):
        question = serializers.CharField(required=True)

    class QuestionDetailOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ("id", "question", "product")

    @extend_schema(request=QuestionDetailInputSerializer, responses=QuestionDetailOutPutSerializer)
    def put(self, reqeust, id: int):
        serializer = self.QuestionDetailInputSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        try:
            question = update_question(
                question_id=id,
                question=serializer.validated_data.get("question"),
                sender=reqeust.user
            )
            return Response(self.QuestionDetailOutPutSerializer(question).data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK:dict})
    def delete(self, request, id: int):
        try:
            delete_question(question_id=id)
            return Response({"message": "سوال با موفقیت حذف گردید"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "مشکلی رخ داده است."}, status=status.HTTP_400_BAD_REQUEST)

class QuestionListOutPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "product", "question", "sender", "answer", "answered", "accepted")

class QuestionListAPIView(ApiAuthMixin, APIView):
    permission_classes = (AdminOrManagerPermission,)

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class QuestionFilterSerializer(serializers.Serializer):
        is_answered = serializers.BooleanField(required=False)

    class PaginationParameterSerializer(serializers.Serializer):
        limit = serializers.IntegerField(required=False)
        offset = serializers.IntegerField(required=False)


    class PaginatedQuestionSerializer(PaginatedSerializer):
        results = QuestionListOutPutSerializer(many=True)
    @extend_schema(parameters=[QuestionFilterSerializer , PaginationParameterSerializer],
                   responses={PaginatedQuestionSerializer})

    def get(self , request):
        filter_serializer = self.QuestionFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        try:
            query = question_list(filters = filter_serializer.validated_data)
        except Exception as error:
            return Response({"error": "مشکلی پیش آمده است."} ,status=status.HTTP_400_BAD_REQUEST)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=QuestionListOutPutSerializer,
            queryset=query,
            view=self,
            request = request
        )


