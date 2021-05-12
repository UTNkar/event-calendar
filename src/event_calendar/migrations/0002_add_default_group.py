# Generated by Django 3.2.2 on 2021-05-11 11:26

from django.db import migrations


def add_default_group(apps, schema_editor):
    Group = apps.get_model('event_calendar', 'Group')
    Group.objects.create(
        name_sv='UTN',
        name_en='UTN'
    )


def remove_default_group(apps, schema_editor):
    Group = apps.get_model('event_calendar', 'Group')
    Group.objects.filter(name_sv='UTN').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('event_calendar', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_default_group,
            reverse_code=remove_default_group
        )
    ]