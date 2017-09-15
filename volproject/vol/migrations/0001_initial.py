# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 00:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=70)),
                ('region', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=70)),
                ('added', models.DateField(verbose_name='date added')),
                ('seen', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=70)),
                ('region', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=70)),
                ('added', models.DateField(verbose_name='date added')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('added', models.DateField(verbose_name='date added')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='labels',
            field=models.ManyToManyField(to='vol.Labels'),
        ),
        migrations.AddField(
            model_name='job',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vol.Organisation'),
        ),
        migrations.AddField(
            model_name='job',
            name='site',
            field=models.ManyToManyField(to='vol.Site'),
        ),
    ]
