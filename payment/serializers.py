from rest_framework import serializers, status

from common.custom_exceptions.custom_exception import CustomException
from common.response.response_information_codes.error_code import ErrorCode
from payment.models import Buyable
from payment.types import PaymentVendor
from user.models import User


class ReceiptVerificationSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(required=True)
    store = serializers.ChoiceField(required=True, choices=PaymentVendor.choices)
    product_key = serializers.CharField(required=True)
    raw_product_data = serializers.JSONField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        metadata = (
            attrs.get("raw_product_data")
            .get("purchasedProduct", {})
            .get("metadata", None)
        )
        receipt = (
            attrs.get("raw_product_data")
            .get("purchasedProduct", {})
            .get("receipt", None)
        )
        if not metadata:
            raise CustomException(
                detail={"metadata": ["Cannot be null or empty"]},
                code=ErrorCode.GENERAL_VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_id = self.context["request"].auth.payload.get("user_id")
        user = User.objects.get(id=user_id)
        validated_data.update({"receipt": receipt})
        return {**validated_data, "user": user}


class BuyableSerializer(serializers.ModelSerializer):
    special_offer_root = serializers.SerializerMethodField()
    title_id = serializers.IntegerField(required=True)
    description_id = serializers.IntegerField(required=True)

    class Meta:
        model = Buyable
        fields = "__all__"
        read_only_fields = (
            "title",
            "description",
        )

    def get_special_offer_root(self, obj):
        if obj.special_offer_root:
            return BuyableSerializer(obj.special_offer_root).data
        else:
            return None
