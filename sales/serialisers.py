from rest_framework import serializers, status
from drf_writable_nested import serializers as writable
from .models import SoldGoods, SalesReceipt
from inventory.serializers import StockSerializer


class ReceiptItemsSerializer(serializers.ModelSerializer):
    product = StockSerializer(many=True)
    # A serialized sold goods list
    class Meta:
        model = SoldGoods
        fields = [
            'receipt_ref', 'product', 'quantity', 'price',
            'amount'
        ]


class SalesReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReceipt
        fields = '__all__'


class ReceiptSerializer(
    writable.NestedUpdateMixin, serializers.ModelSerializer
):
    # Get serialized goods sold for nesting with parent class
    items_set = ReceiptItemsSerializer(many=True)

    class Meta:
        model = SalesReceipt
        # items_set field connected to parent class via related name in model
        fields = [
            'sale_date', 'receipt_number', 'is_credit',
            'credit_account', 'salesman', 'total', 'items_set'
        ]
    
    def create(self, validated_data):
        items_validated_data = validated_data.pop('items_set')
        receipt = SalesReceipt.objects.create(**validated_data)
        items_set_serializer = self.fields['items_set']

        for item in items_validated_data:
            item['receipt'] = receipt
        
        items = items_set_serializer.create(items_validated_data)
        return receipt
