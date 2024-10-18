from rest_framework import serializers
from .models import User, Event, Registration
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
   
    attendees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    waitlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'attendees', 'waitlist', 'no_of_attendees','created_date', "creation_count", "organizer"]
    
    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("The event date cannot be in the past.")
        return value

    def get_attendees_count(self, obj):
        return obj.attendees.count()

    def get_remaining_capacity(self, obj):
        return obj.remaining_capacity()




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'email')
        # extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        read_only_fields = ['id']
    

class RegistrationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Registration
        fields = [ 'user', 'event']
        read_only_fields = ["user",'event']
        