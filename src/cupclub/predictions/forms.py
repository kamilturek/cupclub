from django import forms

from cupclub.predictions.models import Prediction, Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["capper", "subscriber", "channels"]


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ["capper", "content"]
