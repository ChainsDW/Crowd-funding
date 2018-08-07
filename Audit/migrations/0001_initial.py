# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-03 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jiuchai', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.SmallIntegerField(choices=[(0, '第一批次'), (1, '第二批次')])),
                ('advice', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jiuchai.Projects')),
            ],
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='advice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Audit.Audit'),
        ),
    ]