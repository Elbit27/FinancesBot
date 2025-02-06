from rest_framework import serializers
from .models import ReportExpenses, ReportIncomes


# ---------------------------DOHODY----------------------------------

class ReportDailyDListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category_d.name')

    class Meta:
        model = ReportIncomes
        fields = ('id', 'created_at', 'category_name', 'body', 'how_much')


class ReportDailyDCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportIncomes
        fields = '__all__'

    def create(self, validated_data):
        report_daily = ReportIncomes.objects.create(**validated_data)
        return report_daily


class ReportDailyDDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category_d.name')

    class Meta:
        model = ReportIncomes
        fields = '__all__'


# ---------------------------RASHODY---------------------------------

class ReportDailyRListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = ReportExpenses
        fields = ('id', 'created_at', 'category_name', 'body', 'how_much')


class ReportDailyRCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExpenses
        fields = '__all__'

    def create(self, validated_data):
        report_daily = ReportExpenses.objects.create(**validated_data)
        return report_daily


class ReportDailyRDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = ReportExpenses
        fields = '__all__'
