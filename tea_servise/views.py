from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, ListView

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
            new_payment = form.save(commit=False)
            new_payment.staff = form.cleaned_data['staff']
            new_payment.sum_tea = form.cleaned_data['sum_tea']
            new_payment.review = form.cleaned_data['review']
            new_payment.star = form.cleaned_data['star']
            new_payment.save()
            Payment.objects.create(
                staff=new_payment,
                sum_tea=form.cleaned_data['sum_tea'],
                review=form.cleaned_data['review'],
                star=form.cleaned_data['star']
            )
            return HttpResponseRedirect('/leader')
        context = {'form': form}
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

def editLeader(request, id):
    error = ''
    leader = Leader.objects.get(id=id, user=request.user.id)
    if request.method == 'POST':
        form = LeaderCreateForm(request.POST, instance=leader)
        if form.is_valid():
            form.save()
            return redirect('leader')
        else:
            error = 'Форма заполнена некорректно'
    return render(request, 'editLeader.html', {'leader': leader, 'error': error})