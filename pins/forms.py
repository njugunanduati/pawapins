from django import forms
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.auth.models import User
from core.models import TimeStampedModel

from pins.models import Card, CardBatch
from pins.choices import DENOM_CHOICES


class AddCardBatchForm(forms.Form):
    denomination = forms.ChoiceField(choices=DENOM_CHOICES)
    totalcards = forms.IntegerField(required=True, label='Number of cards')

    def clean_denomination(self):
        denomination = self.cleaned_data['denomination']
        if not denomination:
                raise forms.ValidationError("Please select denomination.")
        return denomination


class SearchPinForm(forms.Form):
    serial = forms.IntegerField(required=False, label='Serial')
    pin = forms.IntegerField(required=False, label='Pin')
