# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-28 07:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20170728_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttest',
            name='password',
            field=models.CharField(default='', max_length=255, verbose_name='Пароль для вхождения в тест'),
            preserve_default=False,
        ),
    ]
