from django.contrib import admin

from cupclub.predictions.models import Capper, Subscriber, Subscription


@admin.register(Capper)
class CapperAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
