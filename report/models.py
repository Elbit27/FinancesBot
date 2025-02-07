from django.db import models
from category.models import CategoryIncomes, CategoryExpenses
from django.utils.timezone import localtime


class ReportIncomes(models.Model):
    category = models.ForeignKey(CategoryIncomes, related_name='report_daily_d', null=False, blank=False,
                                 on_delete=models.SET)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=100, null=True,
                            blank=False)
    amount = models.IntegerField(null=False, blank=True)

    class Meta:
        verbose_name = 'Report income'
        verbose_name_plural = 'Report incomes'

    def __str__(self):
        return f"{self.category} - {self.amount} KGS - {localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"


class ReportExpenses(models.Model):
    category = models.ForeignKey(CategoryExpenses, related_name='report_daily_r', null=False, blank=False,
                                 on_delete=models.SET)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=100, null=True,
                            blank=False)
    amount = models.IntegerField(null=False, blank=True)

    class Meta:
        verbose_name = 'Report expense'
        verbose_name_plural = 'Report expenses'

    def __str__(self):
        return f"{self.category} - {self.amount} KGS - {localtime(self.created_at).strftime('%H:%M')}"
