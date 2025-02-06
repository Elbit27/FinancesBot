from rest_framework import serializers
from .models import CategoryExpenses


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExpenses
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExpenses
        fields = '__all__'

