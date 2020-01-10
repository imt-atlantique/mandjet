"""mandjet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from nanogrid.views import IndexView, nanogrid_view
from .views import UserUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('help/', TemplateView.as_view(template_name="help.html"), name='help'),
    path('nanogrid/', nanogrid_view, name='dashboard'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('vehicles/', include('nanogrid.urls')),
    path('signup/', CreateView.as_view(template_name='registration/signup.html',
                                       form_class=UserCreationForm,
                                       success_url='/'), name='signup'),
    path('profile/<int:pk>/', login_required(UserUpdateView.as_view()), name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),

]
