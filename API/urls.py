from django.urls import path, include
from . import views

urlpatterns = [
    # User endpoints
    path('users/', views.UserListAPIView.as_view(), name='user-list'),  # List and create users  
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),  # Retrieve, update, delete user
    
    # Event endpoints
    path('events/', views.EventListAPIView.as_view(), name='event-list'),  # List and create events
    path('events/<int:pk>/', views.EventDetailAPIView.as_view(), name='event-detail'),  # Retrieve, update, delete event
    path('events/upcoming/', views.UpcomingEventListView.as_view(), name='upcoming-event-list'),
    
    # Registration endpoints
     path('register/<int:event_id>/',views.RegisterForEventView.as_view(), name='register-for-event'),

]
