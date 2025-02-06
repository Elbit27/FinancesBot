from django.contrib import admin
from .models import CategoryIncomes, CategoryExpenses

# Register your models here.
admin.site.register(CategoryExpenses)
admin.site.register(CategoryIncomes)
