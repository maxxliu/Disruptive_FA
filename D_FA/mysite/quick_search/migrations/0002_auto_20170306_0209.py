# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-06 02:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quick_search', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Data_Dates',
            new_name='Data_Date',
        ),
        migrations.RenameModel(
            old_name='Fin_Statements',
            new_name='Fin_Statement',
        ),
    ]
