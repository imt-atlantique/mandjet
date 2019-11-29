from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .models import Vehicle, TimeSlot

class IndexView(generic.ListView):
    template_name = 'vehicles/dashboard.html'
    model = Vehicle

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

        messages.success(self.request, _(u"Your booking for %s is ok!") % vehicle)
        return super().form_valid(form)

class TimeSlotIndexView(generic.ListView):
    template_name = 'vehicles/calendar.html'
    model = TimeSlot

    def get_queryset(self):
        return TimeSlot.objects.order_by('-start')[:20]

class TimeSlotDeleteView(generic.DeleteView):
    model = TimeSlot
    success_url = '/'
