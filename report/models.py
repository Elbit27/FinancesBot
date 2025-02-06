from django.db import models
from category.models import CategoryIncomes, CategoryExpenses


class ReportIncomes(models.Model):
    category = models.ForeignKey(CategoryIncomes, related_name='report_daily_d', null=False, blank=False,
                                 on_delete=models.SET)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=100, null=False,
                            blank=False)
    how_much = models.IntegerField(null=False, blank=True)

    class Meta:
        verbose_name = 'Report income'
        verbose_name_plural = 'Report incomes'

    def __str__(self):
        return f'{self.category} - {self.how_much} ({self.body}) {self.created_at.strftime("%H:%M")}'


class ReportExpenses(models.Model):
    category = models.ForeignKey(CategoryExpenses, related_name='report_daily_r', null=False, blank=False,
                                 on_delete=models.SET)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=100, null=False,
                            blank=False)
    how_much = models.IntegerField(null=False, blank=True)

    class Meta:
        verbose_name = 'Report expense'
        verbose_name_plural = 'Report expenses'

    def __str__(self):
        return f'{self.category} - {self.how_much} ({self.body}) {self.created_at.strftime("%I:%M %p")}'
