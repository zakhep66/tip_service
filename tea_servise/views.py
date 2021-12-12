from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, ListView

from .forms import LoginForm, RegistrationForm
from .models import *
from django.contrib.auth.models import Group


def index(request):
    return render(request, 'index.html')


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form, }
        return render(request, 'login.html', context)  # Это страница где будет html форма атворизации

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.user.groups.filter(name='Staff').exists():  # Если чел принадлежит группе name='название группы'
                    # будет редирект на страницу, указанную ниже
                    return HttpResponseRedirect('/staff')  # здесь нужно указать страницу на которую будет редирект
                elif request.user.groups.filter(name='Leader').exists():  # схема таже
                    return HttpResponseRedirect('/leader')
        context = {'form': form}
        return render(request, 'login.html', context)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.phone = form.cleaned_data['phone']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Leader.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            group = Group.objects.get(name='Leader')
            new_user.groups.add(group)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/leader')
        context = {'form': form}
        return render(request, 'registration.html', context)


def staff(request):
    if request.user.groups.filter(name='Staff').exists():
        person = Staff.objects.get(user=request.user.id)
        tips = Payment.objects.filter(staff=person.id)
        sum = 0
        for t in tips:
            sum += t.sum_tea
        return render(request, 'staff.html', {'staff': person, 'tips': tips, 'sum': sum})
    return HttpResponseRedirect('/login')


def leader(request):
    if request.user.groups.filter(name='Leader').exists():
        person = Leader.objects.get(user=request.user.id)
        return render(request, 'leader.html', {'leader': person})
    return HttpResponseRedirect('/login')


# class MeanValue(ListView):
#     model = Payment
#     queryset = Payment.objects.all()
#     template_name = 'staff.html'
#     context_object_name = ['tip_staff']  # в эту переменную будет помещён результат работы класса
#
#     def tip_staff(self, request):
#         user = Staff.objects.get(user=request.user.id)
#         tip = Payment.objects.filter(staff=user.id)
#         return tip
