from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

class UserUpdateView(generic.UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)

    success_url = '/'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)
