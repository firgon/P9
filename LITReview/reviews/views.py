from django.shortcuts import render, redirect
from django.db.models import CharField, Value, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View, DetailView, DeleteView
from django.urls import reverse_lazy

from itertools import chain

from authentication.models import User, UserFollows
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from django.conf import settings


class Home(LoginRequiredMixin, View):
    """class to display main page"""
    login_url = settings.LOGIN_URL
    redirect_field_name = 'redirect_to'
    template_name = 'reviews/home.html'

    def get(self, request):
        tickets = Ticket.objects.filter(
            Q(user__in=request.user.follows.all()) |
            Q(user=request.user)
        )
        # tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.filter(
            Q(user__in=request.user.follows.all()) |
            Q(user=request.user) |
            Q(ticket__user=request.user)
        )
        # reviews  = reviews.annotate(content_type=Value('REVIEW', CharField()))

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
        # tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.all().filter(user=posts_user)
        # reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(chain(reviews, tickets),
                       key=lambda x: x.time_created,
                       reverse=True)

        bool_followed = posts_user in request.user.follows.all()

        return render(request,
                      self.template_name,
                      context={'posts': posts,
                               'posts_user': posts_user,
                               'followed': bool_followed})


class PostReview(LoginRequiredMixin, View):
    """class to display a form to create/modify/delete a review"""
    template = 'reviews/add_review.html'
    pk_url_kwarg = 'ticket_id'

    def get(self, request, ticket_id=None, review_id=None):
        """display a form to create a ticket if there is no ticket in param
        and a form to create a ticket, or to modify a review if param"""
        if ticket_id is None:
            ticket_form = TicketForm()
            ticket = None
        else:
            ticket_form = None
            ticket = Ticket.objects.get(id=ticket_id)

        if review_id is None:
            review_form = ReviewForm()
            review = None
        else:
            review = Review.objects.get(id=review_id)
            review_form = ReviewForm(instance=review)

        return render(request, self.template, {'ticket_form': ticket_form,
                                               'ticket': ticket,
                                               'review_form': review_form,
                                               'review': review})

    def post(self, request, ticket_id=None, review_id=None):
        """register new review with a ticket id or a new created ticket"""
        if review_id is not None:
            review = Review.objects.get(id=review_id)
            review_form = ReviewForm(request.POST, instance=review)
        else:
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
    """Display a form to add or modify a new ticket"""
    model_form = TicketForm
    template_name = 'reviews/add_ticket.html'

    def get(self, request, ticket_id=None):
        if ticket_id is not None:
            ticket = Ticket.objects.get(id=ticket_id)
            form = self.model_form(instance=ticket)
        else:
            form = self.model_form()
            ticket = None

        return render(request, self.template_name, {'form': form,
                                                    'ticket': ticket})

    def post(self, request, ticket_id=None):
        if ticket_id is not None:
            ticket = Ticket.objects.get(id=ticket_id)
            form = self.model_form(request.POST, instance=ticket)
        else:
            form = self.model_form(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Votre ticket a été enregistré.')
            return redirect('ticket-detail', ticket.id)


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    pk_url_kwarg = 'review_id'
    template_name = 'reviews/delete_review.html'
    success_url = reverse_lazy('home')


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = Ticket
    pk_url_kwarg = 'ticket_id'
    template_name = 'reviews/delete_ticket.html'
    success_url = reverse_lazy('home')


class TicketDetail(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'reviews/ticket_detail.html'
    pk_url_kwarg = 'ticket_id'


class ReviewDetail(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    pk_url_kwarg = 'review_id'
