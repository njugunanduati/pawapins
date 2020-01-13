from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel
import architect

@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Subscriber(TimeStampedModel):
    """
     msisdn is the phone number of customer, 
     the meter number and the amount
    """
    msisdn = models.CharField(max_length=20, unique=True)
    meter = models.CharField(max_length=20, null=True,
                             blank=True)
    amount = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.msisdn


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class CardBatch(TimeStampedModel):
    """
     status: 0=pending 1=failed 2=complete
     live: 0=new 1=factory production, 2=disbursed for dist, 3=live,4=canceled
    """
    denomination = models.IntegerField(default=0, blank=True)
    totalcards = models.IntegerField(default=0, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_at = models.DateTimeField(blank=True)
    status = models.IntegerField(default=0, blank=True)
    live = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.denomination)

    @property
    def get_denomination(self):
        return str(self.denomination)


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Card(TimeStampedModel):
    '''
    serial = id/pk
    status: 0=unused  1=used 2=invalid/expired, 3=invalid/caceled
    '''
    pin = models.CharField(max_length=50,unique=True)
    batch = models.ForeignKey(CardBatch, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, blank=True)
    used_by = models.CharField(max_length=20, blank=True, null=True)
    sid = models.CharField(max_length=60, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    used_at = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.pin


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class CardPreview(TimeStampedModel):
    # TODO indenx the pin field
    # printed 0=default 1=printed
    pin = models.CharField(max_length=50, unique=True)
    batch = models.ForeignKey(CardBatch, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, blank=True)
    printed = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.pin
