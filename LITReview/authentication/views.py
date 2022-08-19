from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms


class LoginPageView(View):
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request,
                      self.template_name,
                      context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                return redirect('home')

        message = 'Identifiants invalides.'

        return render(request,
                      self.template_name,
                      context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                return redirect('home')

            message = 'Identifiants invalides.'

    return render(request,
                  'authentication/login.html',
                  context={'form': form, 'message': message})
