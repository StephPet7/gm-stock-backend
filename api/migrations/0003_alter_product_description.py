# Generated by Django 3.2.6 on 2021-09-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210901_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=1500),
        ),
    ]