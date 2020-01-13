from django.contrib import admin

from .models import Subscriber, Card, CardBatch, CardPreview


admin.site.register(Subscriber)
admin.site.register(Card)
admin.site.register(CardBatch)
admin.site.register(CardPreview)

