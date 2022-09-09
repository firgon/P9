from django.db import models
from django.conf import settings


class Ticket(models.Model):
    title = models.CharField(verbose_name="Titre", max_length=128)
    description = models.CharField(max_length=2048)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True,
                              blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title


class Review(models.Model):
    rating_choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    # Main model of this module, store reviews from user
    ticket = models.ForeignKey(to=Ticket,
                               on_delete=models.CASCADE)
    headline = models.CharField(max_length=128,
                                verbose_name="Titre")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Note",
        choices=rating_choices)
    body = models.CharField(max_length=8192,
                            blank=True,
                            verbose_name="Commentaire")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    objects = models.Manager()

    time_created = models.DateTimeField(auto_now_add=True)