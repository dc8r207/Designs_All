# Generated by Django 4.2.4 on 2024-02-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design_progress', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='designers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=20)),
                ('post', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]