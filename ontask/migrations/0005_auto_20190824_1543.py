# Generated by Django 2.2.4 on 2019-08-24 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0004_remove_old_migration_refs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='description_txt',
            new_name='description_text',
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='description_txt',
        ),
        migrations.AddField(
            model_name='plugin',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='action',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='name',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='scheduledaction',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='view',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048),
        ),
    ]
