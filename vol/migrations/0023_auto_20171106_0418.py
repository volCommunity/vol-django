# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 04:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0022_auto_20171106_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.CharField(max_length=4000, null=True),
        ),
    ]