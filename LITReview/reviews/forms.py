from django.forms import ModelForm, Textarea
from .models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ('user', 'time_created')
        widgets = {
            'description': Textarea(attrs={'cols': 50, 'rows': 3}),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'time_created', 'ticket')
        widgets = {
            'body': Textarea(attrs={'cols': 50, 'rows': 3}),
        }
