# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20160111_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.CharField(max_length=250, null=True),
        ),
    ]