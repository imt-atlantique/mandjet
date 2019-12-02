from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'nanogrid'
urlpatterns = [
    path('<uuid:vehicle_id>/book/', login_required(views.TimeSlotCreateView.as_view()), name='book'),
    path('calendar/', views.TimeSlotIndexView.as_view(), name='calendar'),
    path('<uuid:vehicle_id>/bookings/<int:pk>/delete/', login_required(views.TimeSlotDeleteView.as_view()), name='delete'),
    path('<uuid:vehicle_id>/battery/', views.battery_api_view, name='battery_api_view'),
]
