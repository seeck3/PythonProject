# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-27 04:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list', '0002_auto_20180827_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='uploaded_by',
        ),
        migrations.DeleteModel(
            name='Items',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
