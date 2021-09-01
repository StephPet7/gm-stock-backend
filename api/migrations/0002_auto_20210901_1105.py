# Generated by Django 3.2.6 on 2021-09-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='stockUnit',
            field=models.CharField(choices=[('U', 'U'), ('FF', 'Ff'), ('ml', 'Ml'), ('m2', 'M2'), ('m3', 'M3'), ('L', 'L')], default='U', max_length=20),
        ),
    ]