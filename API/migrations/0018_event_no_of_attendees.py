# Generated by Django 5.1.2 on 2024-10-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0017_event_waitlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="no_of_attendees",
            field=models.IntegerField(default=0),
        ),
    ]
