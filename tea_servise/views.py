from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm


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
                if request.user.groups.filter(name='').exists():  # Если чел принадлежит группе name='название группы'
                    # будет редирект на страницу, указанную ниже
                    return HttpResponseRedirect('')  # здесь нужно указать страницу на которую будет редирект
                elif request.user.groups.filter(name='').exists():  # схема таже
                    return HttpResponseRedirect('')
        return render(request, 'login.html', {'form': form})
