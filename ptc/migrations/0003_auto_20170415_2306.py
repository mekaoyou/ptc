# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-15 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ptc', '0002_auto_20170415_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptcuser',
            name='pClass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ptc.PTCClass', verbose_name='\u73ed\u7ea7'),
        ),
        migrations.AlterField(
            model_name='ptcuser',
            name='tel',
            field=models.CharField(max_length=11, verbose_name='\u7535\u8bdd'),
        ),
    ]