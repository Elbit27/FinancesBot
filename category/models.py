from django.db import models


class CategoryExpenses(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'category_expenses'
        verbose_name = 'category_expenses'
        verbose_name_plural = 'categories_expenses'

class CategoryIncomes(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'category_incomes'
        verbose_name = 'category_incomes'
        verbose_name_plural = 'categories_incomes'
