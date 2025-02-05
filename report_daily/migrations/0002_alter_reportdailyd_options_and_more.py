# Generated by Django 5.0.3 on 2024-03-30 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_d_options'),
        ('report_daily', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportdailyd',
            options={},
        ),
        migrations.AlterModelOptions(
            name='reportdailyr',
            options={},
        ),
        migrations.AlterField(
            model_name='reportdailyd',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET, related_name='report_daily_d', to='category.category_d'),
        ),
        migrations.AlterField(
            model_name='reportdailyd',
            name='how_much',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='reportdailyr',
            name='how_much',
            field=models.IntegerField(blank=True),
        ),
    ]
