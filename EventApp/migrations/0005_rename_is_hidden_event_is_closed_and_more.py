# Generated by Django 4.0.4 on 2022-05-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0004_alter_event_max_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_hidden',
            new_name='is_closed',
        ),
        migrations.AlterField(
            model_name='event',
            name='max_number',
            field=models.IntegerField(),
        ),
    ]
