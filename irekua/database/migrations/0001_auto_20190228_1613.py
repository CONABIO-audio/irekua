# Generated by Django 2.1.7 on 2019-02-28 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', 'data_migrations'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='logo',
            field=models.ImageField(blank=True, db_column='logo', help_text='Logo of data collection', null=True, upload_to='images/collections/', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='annotationtype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Annotation type icon', null=True, upload_to='images/annotation_types/', verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='devicebrand',
            name='logo',
            field=models.ImageField(blank=True, db_column='logo', help_text='Logo of device brand', null=True, upload_to='images/device_brands/', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Icon for device type', null=True, upload_to='images/device_types/', verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Event type icon', null=True, upload_to='images/event_types/', verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='logo',
            field=models.ImageField(blank=True, db_column='logo', help_text='Institution logo', null=True, upload_to='images/institutions/', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Item type icon', null=True, upload_to='images/item_types/', verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='licencetype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Licence type icon', null=True, upload_to='images/licence_types/', verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='roletype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Role type icon', null=True, upload_to='images/role_types/', verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='termtype',
            name='icon',
            field=models.ImageField(blank=True, db_column='icon', help_text='Term type icon', null=True, upload_to='images/term_types/', verbose_name='icon'),
        ),
    ]
