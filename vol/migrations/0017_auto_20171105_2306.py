# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-05 23:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0016_auto_20171027_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vol.Organisation'),
        ),
    ]
