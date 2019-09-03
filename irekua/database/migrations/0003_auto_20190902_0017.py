# Generated by Django 2.2.4 on 2019-09-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_devicetype_mime_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='scope',
            field=models.CharField(blank=True, db_column='scope', help_text='Scope of term. Use for disambiguation.', max_length=128, verbose_name='scope'),
        ),
        migrations.AlterUniqueTogether(
            name='term',
            unique_together={('term_type', 'value', 'scope')},
        ),
    ]
