# Generated by Django 3.0 on 2020-07-29 23:15

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=core.utils.update_filename, verbose_name='File'),
        ),
    ]
