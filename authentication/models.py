from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')
    objects = models.Manager()

    class Meta:
        unique_together = [['user', 'followed_user']]


class User(AbstractUser):
    follows = models.ManyToManyField('self',
                                     through=UserFollows,
                                     through_fields=('user', 'followed_user'),
                                     )

