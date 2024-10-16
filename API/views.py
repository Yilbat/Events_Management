from django.shortcuts import render
from rest_framework.response import Response
from .custom_permissions import IsOwnerOrReadOnly, IsOrganizer
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Event, Registration
from .serializers import UserSerializer, EventSerializer, RegistrationSerializer
from django.utils import timezone
from django.contrib import messages
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.urls import reverse
from django.shortcuts import redirect


# Create your views here.

# List and Creat Events


class EventListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(
        date_time__gte=timezone.now())  # Filter upcoming events
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Automatically set the current user as the organizer of the event
    def perform_create(self, serializer):
        # Set the organizer to the current user
        serializer.save(organizer=self.request.user)

# Retrieve, Update, and Delete an individual event


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # Only the organizer can update/delete
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]


class UpcomingEventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        Returns upcoming events and applies optional query filters: title, location, date range.
        """
        queryset = super().get_queryset()
        # Filter by upcoming events
        queryset = queryset.filter(date_time__gte=timezone.now())

        # Get query parameters
        title = self.request.query_params.get('title', None)
        location = self.request.query_params.get('location', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        # Filter by title
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Filter by location
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Filter by date range if both start_date and end_date are provided
        if start_date and end_date:
            queryset = queryset.filter(date_time__range=[start_date, end_date])

        return queryset

# List and create users


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # send to signup page if user is not authenticated

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect unauthenticated users to the registration page
            registration_url = reverse('rest_register')
            return redirect(registration_url)
        
        # If authenticated, proceed with the usual listing of users
        return super().get(request, *args, **kwargs)

# Retrieve, update, and delete individual user

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class RegisterForEventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        user = request.user

        if event.attendees.filter(id=user.id).exists():
            return Response({'message': 'You are already registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        if event.no_of_attendees >= event.capacity:
            event.waitlist.add(user)
            return Response({'message': 'Event is full. You have been added to the waitlist.'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, event=event)

        # Query the Registration model to get the newly created registration instance
        registration = Registration.objects.get(user=user, event=event)

        event.attendees.add(user)
        event.no_of_attendees += 1
        event.save()

        return Response({'message': 'Registration successful.', 'registration': RegistrationSerializer(registration).data}, status=status.HTTP_201_CREATED)
