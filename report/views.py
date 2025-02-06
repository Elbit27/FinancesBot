from rest_framework.viewsets import ModelViewSet
from . import serializers
from .models import ReportIncomes, ReportExpenses


class ReportDailyRViewSet(ModelViewSet):
    queryset = ReportExpenses.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ReportDailyRListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.ReportDailyRCreateUpdateSerializer
        elif self.action in ('destroy', 'retrieve'):
            return serializers.ReportDailyRDetailSerializer


class ReportDailyDViewSet(ModelViewSet):
    queryset = ReportIncomes.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ReportDailyDListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.ReportDailyDCreateUpdateSerializer
        elif self.action in ('destroy', 'retrieve'):
            return serializers.ReportDailyDDetailSerializer
