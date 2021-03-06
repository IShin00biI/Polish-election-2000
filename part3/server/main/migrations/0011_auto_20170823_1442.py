# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 14:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20170821_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='cards',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Karty wydane'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='grabowski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Dariusz Maciej GRABOWSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='ikonowicz',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Piotr IKONOWICZ'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='invalid',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Głosy nieważne'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='kalinowski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Jarosław KALINOWSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='korwin',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Janusz KORWIN-MIKKE'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='krzaklewski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Marian KRZAKLEWSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='kwasniewski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Aleksander KWAŚNIEWSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='lepper',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Andrzej LEPPER'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='lopuszanski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Jan ŁOPUSZAŃSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex='^([^\\W_]|[- ])+$')], verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='olechowski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Andrzej Marian OLECHOWSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='pawlowski',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Bogdan PAWŁOWSKI'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='people',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Uprawnieni'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='subareas',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Obwody'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='walesa',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Lech Wałęsa'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='wilecki',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tadeusz Adam WILECKI'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=32, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^([^\\W_]|[- ])+$')], verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='voivodeship',
            name='name',
            field=models.CharField(max_length=32, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^([^\\W_]|[- ])+$')], verbose_name='Nazwa'),
        ),
    ]
