# Generated by Django 5.1.2 on 2024-10-13 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0010_alter_event_organizer"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="registration",
            unique_together=set(),
        ),
    ]
