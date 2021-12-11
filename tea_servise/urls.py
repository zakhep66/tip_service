from django.template.defaulttags import url
from django.urls import path
from django.views.static import serve

from UP import settings
from . import views
from django.contrib.auth.views import LogoutView

from .views import RegistrationView

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page="login"), name='logout'),
    path('', views.index, name="index"),
    path('staff', views.staff, name="staff"),
    path('registration', views.RegistrationView.as_view(), name="registration"),
]
