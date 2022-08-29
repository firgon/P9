from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms


class LoginPageView(View):
    """login in a class"""
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def dispatch(self, request, *args, **kwargs):
        """override dispatch to redirect authenticated users"""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request,
                      self.template_name,
                      context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
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


class SignupPageView(View):
    """Sign up in a class"""
    form_class = forms.SignupForm
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request,
                      self.template_name,
                      context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        message = "Le formulaire est invalide."
        return render(request,
                      self.template_name,
                      context={"form":form, "message": message})
