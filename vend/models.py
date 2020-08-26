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
	vend_time = models.CharField(max_length=300, null=True) 
	reference = models.CharField(max_length=50, null=True) 
	address = models.TextField(null=True) 
	code = models.CharField(max_length=50, null=True, blank=True)
	token = models.TextField(null=True) 
	units = models.DecimalField(default=0, max_digits=10, decimal_places=2)
	units_type = models.CharField(max_length=150, null=True)
	amount = models.CharField(max_length=30, null=True)
	tax = models.CharField(max_length=30, null=True)
	tarrif = models.CharField(max_length=300, null=True)
	description = models.CharField(max_length=30, null=True)
	rct_num = models.CharField(max_length=30, null=True)
	phone_number = models.CharField(max_length=14, null=True)
	meter = models.CharField(max_length=50, null=True)
	amount_paid = models.CharField(max_length=30, null=True)
	pin = models.CharField(max_length=300, null=True)

	def __str__(self):
		return self.token


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Transaction(TimeStampedModel):
	"""
	table for storing the sequence numbers
	"""
	seq = models.CharField(max_length=5, null=True)

	def __str__(self):
		return self.seq


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Reversal(TimeStampedModel):
	"""
	table for storing the successful reversals
	"""
	vend_rev_time = models.CharField(max_length=300, null=True)
	ref = models.CharField(max_length=300, null=True)
	code = models.CharField(max_length=30, null=True)
	meter = models.CharField(max_length=30, null=True)
	amount = models.CharField(max_length=30, null=True)
	phone_number = models.CharField(max_length=30, null=True)

	def __repr__(self):
		return self.id


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class Sms(TimeStampedModel):
	"""
	table for storing the successful messages received
	"""
	date_received = models.CharField(max_length=300, null=True)
	msisdn = models.CharField(max_length=20, null=True)
	at_id = models.CharField(max_length=300, null=True)
	link_id = models.CharField(max_length=300, null=True)
	cost = models.FloatField(default=0, null=True, blank=True)
	message = models.CharField(max_length=300, null=True)
	to = models.CharField(max_length=300, null=True)
	network_code = models.CharField(max_length=300, null=True)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.message


@architect.install('partition', type='range', subtype='date', constraint='month', column='created')
class SmsSent(TimeStampedModel):
	"""
	table for storing the successful sms messages sent to customer
	"""
	msisdn = models.CharField(max_length=20, null=True)
	message = models.CharField(max_length=300, null=True)
	sent_text = models.CharField(max_length=300, null=True)
	cost = models.CharField(max_length=30, null=True)
	message_id = models.CharField(max_length=300, null=True)

	def __repr__(self):
		return self.id
