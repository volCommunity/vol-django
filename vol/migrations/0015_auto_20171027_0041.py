# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0014_auto_20171026_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='text',
            field=models.CharField(max_length=8000),
        ),
    ]
