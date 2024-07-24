from celery import shared_task
from django.core.mail import send_mail

from cupclub.config.settings import FROM_EMAIL
from cupclub.predictions.enums import Channel
from cupclub.predictions.models import Prediction, Subscription
from cupclub.users.models import User


@shared_task
def send_discord_message(subscriber_id: int, content: str) -> None:
    pass


@shared_task
def send_email_message(subscriber_id: int, content: str) -> None:
    user = User.objects.get(subscriber__id=subscriber_id)

    send_mail(
        subject="CupClub sends you a new prediction",
        from_email=FROM_EMAIL,
        message=content,
        recipient_list=[user.email],
    )


@shared_task
def send_telegram_message(subscriber_id: int, content: str) -> None:
    pass


CHANNEL_TASKS = {
    Channel.DISCORD: send_discord_message,
    Channel.EMAIL: send_email_message,
    Channel.TELEGRAM: send_telegram_message,
}


@shared_task
def send_prediction(prediction_id: int) -> None:
    prediction = Prediction.objects.select_related("capper").get(id=prediction_id)
    subscriptions = Subscription.objects.select_related("subscriber").filter(
        capper_id=prediction.capper.id
    )

    for subscription in subscriptions:
        for channel in subscription.channels:
            CHANNEL_TASKS[channel].delay(subscription.subscriber.id, prediction.content)
