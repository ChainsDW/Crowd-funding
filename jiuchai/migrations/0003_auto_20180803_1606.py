# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-03 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jiuchai', '0002_projects_award'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='award',
            field=models.CharField(max_length=128, verbose_name='回报'),
        ),
    ]