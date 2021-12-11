from django.template.context_processors import static
from django.urls import path

from UP import settings
from . import views
from django.contrib.auth.views import LogoutView

from .views import RegistrationView

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page="login"), name='logout'),
    path('', views.index, name="index"),
    path('staff', views.staff, name="staff"),
    path('leader', views.leader, name="leader"),
    path('registration', views.RegistrationView.as_view(), name="registration"),
]
