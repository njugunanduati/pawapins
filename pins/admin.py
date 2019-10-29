from django.contrib import admin

from .models import Subscriber, CardBatch, CardPreview


admin.site.register(Subscriber)
admin.site.register(CardBatch)
admin.site.register(CardPreview)

