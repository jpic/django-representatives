# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('street', models.CharField(max_length=255, null=True, blank=True)),
                ('number', models.CharField(max_length=255, null=True, blank=True)),
                ('postcode', models.CharField(max_length=255, null=True, blank=True)),
                ('floor', models.CharField(max_length=255, null=True, blank=True)),
                ('office_number', models.CharField(max_length=255, null=True, blank=True)),
                ('kind', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('kind', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('kind', models.CharField(max_length=255, null=True, blank=True)),
                ('short_id', models.CharField(max_length=25, null=True, blank=True)),
                ('url', models.URLField()),
                ('constituency', models.CharField(help_text=b'Authority for which the mandate is realized. Eg.: a eurodeputies has a mandate at the European Parliament for a country', max_length=255, null=True, blank=True)),
                ('role', models.CharField(help_text=b'Eg.: president of a political group at the European Parliament', max_length=25, null=True, blank=True)),
                ('begin_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('active', models.NullBooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=255)),
                ('kind', models.CharField(max_length=255, null=True, blank=True)),
                ('address', models.ForeignKey(to='representatives.Address')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100)),
                ('remote_id', models.CharField(max_length=255, null=True, blank=True)),
                ('first_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.SmallIntegerField(default=0, choices=[(0, b'N/A'), (1, b'F'), (2, b'M')])),
                ('birth_place', models.CharField(max_length=255, null=True, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('cv', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('kind', models.CharField(max_length=255, null=True, blank=True)),
                ('representative', models.ForeignKey(to='representatives.Representative')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='phone',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandate',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='email',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(to='representatives.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
    ]