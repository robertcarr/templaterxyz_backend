# Generated by Django 2.2.16 on 2020-10-15 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0004_auto_20201015_1330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_ative',
            new_name='is_active',
        ),
        migrations.AlterField(
            model_name='user',
            name='api_token',
            field=models.CharField(default='3PCCrcUyt6sxirrMWggcfZqKfh4jHo', max_length=100),
        ),
    ]
