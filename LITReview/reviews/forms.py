from django.forms import ModelForm, IntegerField
from .models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ('user', 'time_created')


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'time_created', 'ticket')

