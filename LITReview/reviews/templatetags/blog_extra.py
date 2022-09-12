from django import template

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def is_review(instance):
    """Returns if an instance is a REVIEW or not"""
    return type(instance).__name__ == "Review"


@register.filter
def is_ticket(instance):
    """Returns if an instance is a TICKET or not"""
    return type(instance).__name__ == "Ticket"
