# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 20:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='commune',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Area'),
        ),
    ]
