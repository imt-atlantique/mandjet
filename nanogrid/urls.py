from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'nanogrid'
urlpatterns = [
    path('<uuid:vehicle_id>/book/', login_required(views.TimeSlotCreateView.as_view()), name='book'),
    path('<uuid:vehicle_id>/report/', login_required(views.ReportIssueView.as_view()), name='report'),
    path('calendar/', views.TimeSlotIndexView.as_view(), name='calendar'),
    path('calendar.ics', views.ics_api_view, name='ics_api_view'),
    path('<uuid:vehicle_id>/bookings/<int:pk>/', login_required(views.TimeSlotUpdateView.as_view()), name='update'),
    path('<uuid:vehicle_id>/bookings/<int:pk>/delete/', login_required(views.TimeSlotDeleteView.as_view()), name='delete'),
    path('<uuid:vehicle_id>/battery/', views.battery_api_view, name='battery_api_view'),
]
