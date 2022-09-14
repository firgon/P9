from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from .models import UserFollows, User


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
                      context={"form": form, "message": message})


class Follow(LoginRequiredMixin, View):
    model = UserFollows
    redirect_url = 'following'

    def get(self, request, user_id):
        followed_user = User.objects.get(id=user_id)
        follow = self.model()
        follow.user = request.user
        follow.followed_user = followed_user
        follow.save()
        messages.success(request, f"Vous suivez à présent {followed_user.username}.")
        return redirect(self.redirect_url)


class UnFollow(LoginRequiredMixin, View):
    model = UserFollows
    redirect_url = 'following'

    def get(self, request, user_id):
        followed_user = User.objects.get(id=user_id)
        relation = self.model.objects.get(user=request.user, followed_user=followed_user)
        relation.delete()
        messages.success(request, f"Vous ne suivez plus {followed_user.username}.")
        return redirect(self.redirect_url)


class Following(LoginRequiredMixin, View):
    model = UserFollows
    template_name = "authentication/following.html"

    def get(self, request):
        followed_users = request.user.follows.all()
        all_users = User.objects.all()

        users = [user.username for user in all_users if user not in followed_users and user != request.user]

        # all_usernames = [user.username for user in all_users]
        return render(request, self.template_name, {'users': users, 'followed_users': followed_users})

    def post(self, request):
        try:
            followed_user = User.objects.get(username=request.POST['user'])
            return redirect('follow', user_id=followed_user.id)
        except:
            messages.error(request, f"{request.POST['user']} ne semble pas être un utilisateur du site.")
            return redirect('following')

