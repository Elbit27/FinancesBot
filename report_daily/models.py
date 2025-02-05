from django.db import models
from time import strftime
from category.models import Category, Category_d


class ReportDailyD(models.Model):
    category = models.ForeignKey(Category_d, related_name='report_daily_d', null=False, blank=False,
                                 on_delete=models.SET)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=100, null=False,
                            blank=False)
    how_much = models.IntegerField(null=False, blank=True)

    class Meta:
        verbose_name = 'Report daily dohod'
        verbose_name_plural = 'Report daily dohody'

    def __str__(self):
        return f'{self.category} - {self.how_much} ({self.body}) {self.created_at.strftime("%H:%M")}'


class ReportDailyR(models.Model):
    category = models.ForeignKey(Category, related_name='report_daily_r', null=False, blank=False,
                                 on_delete=models.SET)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=100, null=False,
                            blank=False)
    how_much = models.IntegerField(null=False, blank=True)

    class Meta:
        verbose_name = 'Report daily rashod'
        verbose_name_plural = 'Report daily rashody'

    def __str__(self):
        return f'{self.category} - {self.how_much} ({self.body}) {self.created_at.strftime("%I:%M %p")}'
