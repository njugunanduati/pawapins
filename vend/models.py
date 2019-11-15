from django.db import models


import uuid
import string
import random

from datetime import datetime
from hashlib import md5
from time import time
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from django.conf import settings
import architect



@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Token(TimeStampedModel):
	"""
	table for storing the successful bought tokens
	"""
	vend_time = models.CharField(max_length=300, null=False) 
	reference = models.CharField(max_length=50, null=False) 
	address = models.CharField(max_length=150, null=False) 
	token = models.CharField(max_length=150, null=False) 
	units = models.CharField(max_length=150, null=False)
	units_type = models.CharField(max_length=150, null=False)
	amount = models.CharField(max_length=30, null=False)
	tax = models.CharField(max_length=30, null=False)
	tarrif = models.CharField(max_length=300, null=False)
	description = models.CharField(max_length=30, null=False)
	rct_num = models.CharField(max_length=30, null=False)
	phone_number = models.CharField(max_length=14, null=True)
	meter = models.CharField(max_length=50, null=False)
	amount_paid = models.CharField(max_length=30, null=False)
	pin = models.CharField(max_length=300, null=False)

	def __repr__(self):
		return self.id


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Reversal(TimeStampedModel):
	"""
	table for storing the successful reversals
	"""
	vend_rev_time = models.CharField(max_length=300, null=True)
	ref = models.CharField(max_length=300, null=False)
	code = models.CharField(max_length=30, null=False)
	meter = models.CharField(max_length=30, null=False)
	amount = models.CharField(max_length=30, null=False)
	phone_number = models.CharField(max_length=30, null=False)

	def __repr__(self):
		return self.id



@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Sms(TimeStampedModel):
	"""
	table for storing the successful messages recieved
	"""
	date_recieved = models.CharField(max_length=300, null=True)
	msisdn = models.CharField(max_length=20, null=True)
	at_id = models.CharField(max_length=300, null=True)
	link_id = models.CharField(max_length=300, null=True)
	cost = models.FloatField(default=0, null=True, blank=True)
	message = models.CharField(max_length=300, null=True)
	to = models.CharField(max_length=300, null=False)
	network_code = models.CharField(max_length=300, null=False)

	def __repr__(self):
		return self.id


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class SmsSent(TimeStampedModel):
	"""
	table for storing the successful sms messages sent to customer
	"""
	msisdn = models.CharField(max_length=20, null=True)
	message = models.CharField(max_length=300, null=False)
	cost = models.CharField(max_length=30, null=False)
	status = models.CharField(max_length=30, null=False)
	message_id = models.CharField(max_length=300, null=False)

	def __repr__(self):
		return self.id
