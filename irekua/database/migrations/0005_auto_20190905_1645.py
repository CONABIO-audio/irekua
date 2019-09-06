# Generated by Django 2.2.5 on 2019-09-05 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20190903_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='captured_on_timezone',
            field=models.CharField(blank=True, db_column='captured_on_timezone', help_text='Timezone corresponding to date fields', max_length=256, null=True, verbose_name='timezone'),
        ),
        migrations.AlterField(
            model_name='collectiondevice',
            name='internal_id',
            field=models.CharField(blank=True, db_column='internal_id', help_text='ID of device within the collection (visible to all collection users)', max_length=64, verbose_name='ID within collection'),
        ),
        migrations.AlterField(
            model_name='collectionsite',
            name='internal_id',
            field=models.CharField(blank=True, db_column='internal_id', help_text='ID of site within the collection (visible to all collection users)', max_length=64, verbose_name='ID within collection'),
        ),
        migrations.AlterField(
            model_name='physicaldevice',
            name='identifier',
            field=models.CharField(blank=True, db_column='identifier', help_text='Simple device identifier (visible only to owner)', max_length=128, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(blank=True, db_column='name', help_text='Name of site (visible only to owner)', max_length=128, null=True, verbose_name='name'),
        ),
    ]