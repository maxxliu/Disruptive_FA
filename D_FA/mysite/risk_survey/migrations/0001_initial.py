# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-09 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rm_id', models.IntegerField()),
                ('risk', models.DecimalField(decimal_places=5, max_digits=6)),
            ],
        ),
    ]