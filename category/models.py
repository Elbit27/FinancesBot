from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Category_d(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'category_d'
        verbose_name = 'category_d'
        verbose_name_plural = 'categories_d'
