# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-24 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20171211_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergeokey',
            name='nickname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
