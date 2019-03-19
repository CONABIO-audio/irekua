# Generated by Django 2.1.7 on 2019-03-19 19:41

import database.utils
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='filesize',
            field=models.IntegerField(blank=True, db_column='filesize', help_text='Size of resource in Bytes', verbose_name='file size'),
        ),
        migrations.AlterField(
            model_name='item',
            name='hash',
            field=models.CharField(blank=True, db_column='hash', help_text='Hash of resource file', max_length=64, unique=True, verbose_name='hash'),
        ),
        migrations.AlterField(
            model_name='item',
            name='licence',
            field=models.ForeignKey(blank=True, db_column='licence_id', help_text='Licence of item', on_delete=django.db.models.deletion.PROTECT, to='database.Licence', verbose_name='licence'),
        ),
        migrations.AlterField(
            model_name='item',
            name='media_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_column='media_info', default=database.utils.empty_JSON, help_text='Information of resource file', verbose_name='media info'),
        ),
        migrations.AlterField(
            model_name='site',
            name='site_type',
            field=models.ForeignKey(db_column='site_type', default='generic site', help_text='Type of site', on_delete=django.db.models.deletion.PROTECT, to='database.SiteType', verbose_name='site type'),
        ),
    ]
