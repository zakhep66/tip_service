from django.template.context_processors import static
from django.urls import path

from UP import settings
from . import views
from django.contrib.auth.views import LogoutView

from .views import RegistrationView

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page="login"), name='logout'),
    path('index', views.index, name="index"),
    path('', views.AddPaymentView.as_view(), name="index"),
    path('staff', views.staff, name="staff"),
    path('leader', views.leader, name="leader"),
    path('add-staff/<int:branch>/', views.AddStaff.as_view(), name="add_staff"),
    path('registration', views.RegistrationView.as_view(), name="registration"),
    path('add-branch', views.AddBranch.as_view(), name="add_branch"),
    path('editLeader/<int:id>', views.editLeader, name="editLeader"),
    path('editBranch/<int:id>', views.editBranch, name="edit_branch"),
    path('editStaff/<int:id>', views.editStaff, name="editStaff"),

]
