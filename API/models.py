from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    creation_count = models.IntegerField(default=0)  # Field to track instance creation
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)
    waitlist = models.ManyToManyField(User, related_name='waitlisted_events', blank=True)
    no_of_attendees = models.IntegerField(default=0)

    def clean(self):
        # Prevent creation of events in the past
        if self.date_time < timezone.now():
            raise ValidationError("The event date cannot be in the past.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Call clean to validate date before savings
        super(Event, self).save(*args, **kwargs)
    
    """Check if the event has reached its maximum capacity."""
    def is_full(self):
        return self.attendees.count() >= self.capacity

    def remaining_capacity(self):
        """Calculate the number of spots remaining."""
        return self.capacity - self.attendees.count()
    
    def __str__(self):
        return self.title
    

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name= "event_register")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_register")