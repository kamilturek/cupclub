from typing import Any, Self

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from cupclub.predictions.enums import Channel
from cupclub.predictions.forms import PredictionForm, SubscriptionForm
from cupclub.predictions.models import Capper, Subscriber, Subscription
from cupclub.predictions.tasks import send_prediction


class CapperListView(ListView):
    model = Capper

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["subscribed_capper_ids"] = self._get_subscribed_capper_ids()
        return context

    # Really bad practice to mix a generic list view with another POST handler.
    # Done as a shortcut for MVP only and due to time constraints :)
    def post(self, request: HttpRequest, *args: Any, **kwrags: Any) -> HttpResponse:
        # Missing validation if the user is creating a subscription for themselves.
        data = request.POST.copy()
        data["channels"] = []

        for channel in Channel:
            if data.get(channel) == "on":
                data["channels"].append(channel)

        form = SubscriptionForm(data)

        if not form.is_valid():
            messages.error(request, form.errors)
            return self.get(request)

        form.save()
        return self.get(request)

    def _get_subscribed_capper_ids(self: Self) -> set[int]:
        try:
            return set(
                Subscription.objects.filter(
                    subscriber_id=self.request.user.subscriber.id
                ).values_list("capper_id", flat=True)
            )
        except ObjectDoesNotExist:
            return set()


class SubscriberListView(ListView):
    model = Subscriber

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(subscriptions__capper_id=self.request.user.capper.id)
        )

    def post(self, request: HttpRequest, *args: Any, **kwrags: Any) -> HttpResponse:
        form = PredictionForm(request.POST)

        if not form.is_valid():
            messages.error(request, form.errors)
            return self.get(request)

        prediction = form.save()
        send_prediction.delay(prediction.id)

        messages.success(
            request,
            "Prediction sent.",
        )

        return self.get(request)
