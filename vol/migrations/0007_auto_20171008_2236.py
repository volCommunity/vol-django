# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0006_auto_20171003_0219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='added',
        ),
        migrations.RemoveField(
            model_name='labels',
            name='added',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='added',
        ),
        migrations.RemoveField(
            model_name='site',
            name='added',
        ),
        migrations.AddField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='labels',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labels',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organisation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='site',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]