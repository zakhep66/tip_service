from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, ListView
import datetime

from .forms import *
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
                if request.user.groups.filter(
                        name='Staff').exists():  # Если чел принадлежит группе name='название группы'
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
        rating = 0
        count_rating = 0
        count_sum_tea = 0
        sum_tea = 0
        for t in tips:
            sum += t.sum_tea
            if t.rating is not None:
                count_rating += 1
                rating += t.rating
            if t.sum_tea is not None:
                count_sum_tea += 1
                sum_tea += t.sum_tea
        try:
            average_rating = int(rating / count_rating * 10) / 10
            average_sum_tea = int(sum_tea / count_sum_tea * 100) / 100
        except ZeroDivisionError:
            average_rating = 0
            average_sum_tea = 0
        return render(request, 'staff.html',
                      {'staff': person, 'tips': tips, 'sum': sum, 'average_rating': average_rating,
                       'average_sum_tea': average_sum_tea})
    return HttpResponseRedirect('/login')


def leader(request):
    if request.user.groups.filter(name='Leader').exists():
        person = Leader.objects.get(user=request.user.id)

        # создание словаря из филиалов и работающих там сотрудников
        branches = Branch.objects.filter(leader=person.id)
        branch_staff = []
        for b in branches:
            staff_list = Staff.objects.filter(id_branch=b.id)
            for s in staff_list:
                branch_staff.append(s)

        return render(request, 'leader.html', {'leader': person, 'branches': branches, 'branch_staff': branch_staff})
    return HttpResponseRedirect('/login')


class AddPaymentView(View):

    def get(self, request, *args, **kwargs):
        form = PaymentForm(request.POST or None)
        context = {'form': form}
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            error = str(form.errors)
        context = {'form': form, 'error': error}
        return render(request, 'index.html', context)


class AddBranch(View):

    def get(self, request):
        form = AddBranchForm
        context = {'form': form}
        return render(request, 'branch.html', context)

    def post(self, request):
        form = AddBranchForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('index')
        context = {'form': form}
        return render(request, 'branch.html', context)


class AddStaff(View):

    def get(self, request, branch):
        form = AddStaffForm
        branch = Branch.objects.get(id=branch)
        context = {'form': form, 'branch': branch}
        return render(request, 'staff_add.html', context)

    def post(self, request, branch):
        form_staff = AddStaffForm(request.POST or None)
        branch = Branch.objects.get(id=branch)
        last_id = User.objects.latest('id').id
        generate_username = 'user' + str(last_id)
        form_user = UserCreateForm(
            {'password': request.POST['password'], 'confirm_password': request.POST['confirm_password'],
             'last_login': str(datetime.datetime.now()), 'username': generate_username,
             'date_joined': str(datetime.datetime.now()), 'is_active': True})

        if form_user.is_valid() and form_staff.is_valid():
            with transaction.atomic():
                user_instance = form_user.save(commit=False)
                group = Group.objects.get(name='Staff')
                user_instance.save()
                user_instance.groups.add(group)
                user_instance.set_password(form_user.cleaned_data['password'])
                user_instance.save()
                staff_instance = form_staff.save(commit=False)
                staff_instance.user = user_instance
                staff_instance.id_branch = branch
                staff_instance.save()

            return redirect('leader')
        else:
            error = str(form_user.errors) + str(form_staff.errors)

        context = {'form': form_staff, 'error': error}
        return render(request, 'staff_add.html', context)
