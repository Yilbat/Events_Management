# Generated by Django 5.1.2 on 2024-10-13 16:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0012_alter_registration_unique_together"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="waitlist",
            name="event",
        ),
        migrations.RemoveField(
            model_name="waitlist",
            name="user",
        ),
        migrations.AddField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(
                blank=True, related_name="attending_events", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="waitlist",
            field=models.ManyToManyField(
                blank=True,
                related_name="waitlisted_events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="Registration",
        ),
        migrations.DeleteModel(
            name="Waitlist",
        ),
    ]
