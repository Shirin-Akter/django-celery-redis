# Generated by Django 3.1.3 on 2020-11-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=None),
        ),
    ]