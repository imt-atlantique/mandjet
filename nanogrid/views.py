from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import Vehicle, TimeSlot, Issue

import json
import datetime
from icalendar import Calendar, Event

class IndexView(generic.ListView):
    template_name = 'vehicles/dashboard.html'
    model = Vehicle

    ordering = ['-id']

class TimeSlotCreateView(generic.CreateView):
    model = TimeSlot
    fields = ['start', 'end']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('vehicle_id'))
        context['vehicle'] = vehicle

        return context

    def form_valid(self, form):
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('vehicle_id'))
        form.instance.vehicle = vehicle
        form.instance.user = self.request.user

        timeslot_conflict = TimeSlot.objects.filter(vehicle=vehicle, start__lte=form.instance.end, end__gte=form.instance.start).first()
        if timeslot_conflict or form.instance.start > form.instance.end:
            messages.error(self.request, _(u"%s is not available for this period") % vehicle)
            form.instance.end = form.instance.start
            return super().form_valid(form)
        else:
            messages.success(self.request, _(u"Your booking for %s is ok!") % vehicle)
            return super().form_valid(form)

        messages.success(self.request, _(u"Your booking for %s is ok!") % vehicle)
        return super().form_valid(form)

class TimeSlotIndexView(generic.ListView):
    template_name = 'vehicles/calendar.html'
    model = TimeSlot

    def get_queryset(self):
        return TimeSlot.objects.order_by('-start')[:10]

class TimeSlotUpdateView(generic.UpdateView):
    model = TimeSlot
    fields = ['start', 'end']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('vehicle_id'))
        context['vehicle'] = vehicle

        return context

class ReportIssueView(generic.CreateView):
    model = Issue
    fields = ['comment',]
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('vehicle_id'))
        context['vehicle'] = vehicle

        return context

    def form_valid(self, form):
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('vehicle_id'))
        form.instance.vehicle = vehicle
        form.instance.user = self.request.user

        messages.success(self.request, _(u"Your issue for %s has been reported!") % (vehicle.name[0].lower() + vehicle.name[1:]))

        send_mail(
            _(u"An issue for %s has been reported!") % (vehicle.name[0].lower() + vehicle.name[1:]),
            _(u"Here is the comment: %s") % form.instance.comment,
            'support@mandjet.fr',
            ['baptiste@lenuage.io'],
            fail_silently=False,
        )
        return super().form_valid(form)

class TimeSlotDeleteView(generic.DeleteView):
    model = TimeSlot
    success_url = '/'

@csrf_exempt
def battery_api_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('battery'):
            vehicle.battery = data.get('battery')
            vehicle.save()
    response={
        'id': vehicle.id,
        'battery': vehicle.battery,
    }
    return JsonResponse(response)

@csrf_exempt
def status_api_view(request):
    vehicles = Vehicle.objects.all()

    vehicles_status = []
    for vehicle in vehicles:
        vehicles_status.append({
            "id":vehicle.id, 
            "name":vehicle.name, 
            "type":vehicle.type, 
            "is_available":bool(vehicle.is_available()),
            "next_ts":{"start":vehicle.next_ts().start, "end":vehicle.next_ts().end, "user":vehicle.next_ts().user.first_name} if vehicle.next_ts() else None,
            "battery":vehicle.battery
        })

    return JsonResponse(vehicles_status, safe=False)

@csrf_exempt
def ics_api_view(request):
    timeslots = TimeSlot.objects.all()

    calendar = Calendar()
    calendar.add('prodid', '-//IMT Atlantique//NONSGML Mandjet vehicles calendar//EN')
    calendar.add('version', '2.0')

    for timeslot in timeslots:
        event = Event()
        event.add('summary', str(timeslot.vehicle) + ' - ' + timeslot.user.first_name)
        event.add('dtstart', timeslot.start)
        event.add('dtend', timeslot.end)
        event.add('dtstamp', timeslot.created_date)

        calendar.add_component(event)

    return HttpResponse(calendar.to_ical(), content_type='text/calendar')

def nanogrid_view(request):
    forecasts_file = open('nanogrid/forecast.solar/latest.json')
    forecasts = json.load(forecasts_file)

    forecasts = forecasts.get('result')
    production = {}

    now = timezone.now()

    current_forecast = 0
    for k, v in forecasts.items():
        d = datetime.datetime.strptime(k, '%Y-%m-%d %H:%M:%S')
        if d.timestamp() < now.timestamp():
            production[k] = int(v/13)
        if k.startswith(now.strftime('%Y-%m-%d %H')):
            current_forecast = v

    context = {
            'forecasts': forecasts,
            'production': production,
            'current_forecast': current_forecast,
            'current_production': current_forecast/13,
            }
    return render(request, 'nanogrid/dashboard.html', context)
