from typing import Self

from django.contrib.postgres.fields import ArrayField
from django.db import models

from cupclub.predictions.enums import Channel
from cupclub.users.models import User


class Capper(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    bio = models.TextField(
        blank=True,
    )

    def __str__(self: Self) -> str:
        return self.user.username


class Subscriber(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self: Self) -> str:
        return self.user.username


class Subscription(models.Model):
    capper = models.ForeignKey(
        Capper,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    channels = ArrayField(
        models.CharField(
            max_length=16,
            choices=Channel.choices,
        ),
    )

    def __str__(self: Self) -> str:
        return f"{self.capper} / {self.subscriber}"


class Prediction(models.Model):
    # Probably CASCADE is not a good idea.
    # Data should be archived instead.
    capper = models.ForeignKey(
        Capper,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
