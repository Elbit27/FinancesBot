from django.contrib import admin

from .models import ReportExpenses, ReportIncomes


admin.site.register(ReportIncomes)
admin.site.register(ReportExpenses)
