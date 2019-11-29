from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Vehicle(models.Model):
    name = models.CharField(_(u'Name'), max_length=32, default=_('My e-scooter'))

    VEHICLE_TYPE = (
        (0, _('Scooter')),
        (1, _('Bike')),
        (2, _('Scooter (motorcycle)')),
    )

    type = models.PositiveSmallIntegerField(_("Vehicle "), choices=VEHICLE_TYPE, default=1)
    serial_number = models.SlugField(_("Serial Number"))
    battery = models.PositiveSmallIntegerField(_("Battery status"), validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    image = models.ImageField(_('Picture'), upload_to='uploads/', blank=True)

    created_date = models.DateTimeField(_('Date created'), auto_now_add=True)

    def __str__(self):
        return self.name

    def is_available(self):
        return not TimeSlot.objects.filter(vehicle=self, start__lte=timezone.now(), end__gte=timezone.now()).count() > 0

    def next_ts(self):
        return TimeSlot.objects.filter(vehicle=self, end__gte=timezone.now()).first()

    is_available.boolean = True
    is_available.short_description = _('Available?')

class TimeSlot(models.Model):
    start = models.DateTimeField(_('Start time'))
    end = models.DateTimeField(_('End time'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    created_date = models.DateTimeField(_('Date created'), auto_now_add=True)
