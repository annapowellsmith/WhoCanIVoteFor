# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20160323_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Post'),
        ),
    ]
