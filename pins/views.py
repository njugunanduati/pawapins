import json
import random
import string
import logging
import io
import csv

from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic.base import View
from django.contrib.auth.models import User
from twisted.internet import reactor

from pins.models import Card, CardBatch, CardPreview
from pins.forms import AddCardBatchForm, SearchPinForm
from pins import utils



class BatchView(LoginRequiredMixin, TemplateView):
    template_name = "batch.html"
    title = 'Batch'

    def get_context_data(self, **kwargs):
        context = super(BatchView, self).get_context_data(**kwargs)
        context["batch"] = CardBatch.objects.all()
        context["title"] = self.title
        return context


class AddBatchView(LoginRequiredMixin, TemplateView):
    template_name = "add_batch.html"
    form = AddCardBatchForm
    title = "Add Batch"

    def get_context_data(self, **kwargs):
        context = super(AddBatchView, self).get_context_data(**kwargs)
        context["form"] = self.form
        context["title"] = self.title
        return context
    
    def post(self, request):
        form = AddCardBatchForm(data=request.POST)
        user = request.user
        if form.is_valid():
            data = form.cleaned_data
            denomination = data['denomination']
            totalcards = int(form.data['totalcards'])
            expire_at = datetime.now()+timedelta(days=365*2)
            card_batch = CardBatch(denomination=denomination,totalcards=totalcards,
                                live=0, expire_at=expire_at, status=0, created_by=user)
            card_batch.save()
            reactor.callInThread(utils.generate_cards, totalcards, card_batch)
            messages.success(request,"Cards are being generated, please wait")
            return HttpResponseRedirect(reverse('pins:batch'))
        else:
            return self.render_to_response(self.get_context_data(
                form=form,
            ))


class ShowPinsView(LoginRequiredMixin, TemplateView):
    template_name = "pins.html"
    title = "Show Pins"
    form = SearchPinForm
    pins = Card.objects.all()

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page')
        context = super(ShowPinsView, self).get_context_data(**kwargs)
        context["form"] = self.form
        context["title"] = self.title
        paginator = Paginator(self.pins, 10)
        pins = paginator.get_page(page)
        context["pins"] = pins
        return context
    
    def post(self, request, id):
        form = AddCardBatchForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            serial = data["serial"]
            pin = data["pin"]
            if serial:
                pins = pins.filter(id__startswith=serial)
            elif pin:
                pins = pins.filter(pin__startswith=pin)
            pins = pins.order_by('id')
            return self.render_to_response(self.get_context_data(
                form=form, pins=pins
            ))
        else:
            return HttpResponseRedirect(reverse('pins:batch'))

@login_required
def move_to_live(request, id):
    try:
        pins = None
        batch = CardBatch.objects.get(id=id)
        if not batch.live:
            pins = CardPreview.objects.filter(batch=batch, status=0)
            if pins:
                for pin in pins:
                    card = Card(id=pin.id, pin=pin.pin, created_at=pin.created, batch=pin.batch, active=True, status=0, used_at=datetime(2017, 7, 1))
                    card.save()
                batch.live = 3
                batch.save()
                messages.success(request, "Pins have been moved to live")
            else:
                messages.warning(request, "%s batch found" % str(id))
        else:
            messages.warning(request, "%s batch id not found" % str(id))
        return HttpResponseRedirect(reverse('pins:batch'))
    except Exception as e:
        print("Error as ", str(e))
        logging.exception(e)


@login_required
def print_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="active_pins.csv"'

    writer = csv.writer(response)
    writer.writerow(['Pin', 'Amount'])
    cards = Card.objects.filter(pin=pin, status=0).all()
    for card in cards:
        writer.writerow([card.pin, card.batch.denomination])

    return response