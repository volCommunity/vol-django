# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0015_auto_20171027_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='text',
            field=models.TextField(),
        ),
    ]
