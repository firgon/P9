from django.shortcuts import render, redirect
from django.db.models import CharField, Value
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View, DetailView

from itertools import chain
from authentication.models import User
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows
from django.conf import settings


class Home(LoginRequiredMixin, View):
    """class to display main page"""
    login_url = settings.LOGIN_REDIRECT_URL
    redirect_field_name = 'redirect_to'
    template_name = 'reviews/home.html'

    def get(self, request):
        tickets = Ticket.objects.all().filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.all().filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(chain(reviews, tickets),
                       key=lambda x: x.time_created,
                       reverse=True)

        return render(request, self.template_name, {'posts': posts})


class PostsList(LoginRequiredMixin, View):
    """class to display all posts (reviews and tickets) from a user"""

    template_name = 'reviews/posts.html'

    def get(self, request, user_id=None):
        if user_id is None:
            user_id = request.user.id

        posts_user = User.objects.get(id=user_id)

        tickets = Ticket.objects.all().filter(user=posts_user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.all().filter(user=posts_user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(chain(reviews, tickets),
                       key=lambda x: x.time_created,
                       reverse=True)


        return render(request,
                      self.template_name,
                      context={'posts': posts,
                               'posts_user': posts_user,
                               # TODO
                               'followed': False})


class AddTicketReview(LoginRequiredMixin, View):
    """class to display a form to create a review WITHOUT ticket"""
    template = 'reviews/add_review.html'
    pk_url_kwarg = 'ticket_id'

    def get(self, request, ticket_id=None):
        """display a form to create a ticket if there is no ticket in param"""
        if ticket_id is None:
            ticket_form = TicketForm()
            ticket = None
        else:
            ticket_form = None
            ticket = Ticket.objects.get(id=ticket_id)

        review_form = ReviewForm()
        return render(request, self.template, {'ticket_form': ticket_form,
                                               'ticket': ticket,
                                               'review_form': review_form})

    def post(self, request, ticket_id=None):
        """register new review with a ticket id or a new created ticket"""
        review_form = ReviewForm(request.POST)
        ticket = None

        if ticket_id is None:
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
        else:
            ticket = Ticket.objects.get(id=ticket_id)

        if review_form.is_valid() and ticket is not None:
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Votre review a été enregistrée.')
            return redirect('review-detail', review.id)


class AddTicket(LoginRequiredMixin, View):
    """Display a form to add a new ticket"""
    model_form = TicketForm
    template_name = 'reviews/add_ticket.html'

    def get(self, request):
        form = self.model_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.model_form(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Votre ticket a été enregistré.')
            return redirect('ticket-detail', ticket.id)


class TicketDetail(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'reviews/ticket_detail.html'
    pk_url_kwarg = 'ticket_id'


class ReviewDetail(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    pk_url_kwarg = 'review_id'


class Follow(LoginRequiredMixin, View):
    model = UserFollows

    def get(self, request, user_id):
        followed_user = User.objects.get(id=user_id)
        follow = self.model()
        follow.user = request.user
        follow.followed_user = followed_user
        follow.save()
        return redirect('home')

