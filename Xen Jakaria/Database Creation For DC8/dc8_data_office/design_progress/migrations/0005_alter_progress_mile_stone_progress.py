# Generated by Django 4.2.4 on 2024-02-29 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design_progress', '0004_progress_mile_stone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress_mile_stone',
            name='progress',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
    ]