# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-27 21:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Ответ.')),
                ('is_valid', models.BooleanField(default=False, verbose_name='Правильный ли ответ?')),
            ],
            options={
                'verbose_name_plural': 'Ответы',
                'verbose_name': 'Ответ',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название категории')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активна ли категория?')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'verbose_name': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.PositiveSmallIntegerField(choices=[(1, 'Junior'), (2, 'Middle'), (3, 'Senior'), (4, 'Other')], default=4, verbose_name='Сложность вопроса')),
                ('question', models.TextField(verbose_name='Вопрос')),
                ('is_active', models.BooleanField(default=False, verbose_name='Доступен ли вопрос?')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Category')),
            ],
            options={
                'verbose_name_plural': 'Вопросы',
                'verbose_name': 'Вопрос',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.Question'),
        ),
    ]
