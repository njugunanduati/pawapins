#!/usr/bin/python3
import json
import sys
import pytz
import time
import random
import socket
from lxml import etree
from .utils import wrap, un_wrap, get_rand

my_ref = get_rand()


class IpayConnect:
	"""
	The class to make the socket connection 
	and vend the electricity token
	"""
	def __init__(self, ip, port, client, term, meter, amount, today, my_ref):
		self.ip = ip
		self.port = int(port)
		self.client = client
		self.term = term
		self.meter = meter
		self.amount = int(amount) * 100
		self.today = today
		self.my_ref = my_ref

	def create_socket(self):
		"""
		create the socket connection
		"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Socket successfully created")
			s.connect((self.ip, self.port))
			print("Socket connected to {} on port {}".format(self.ip, self.port))
			return s
		except Exception as e:
			return str(e)


	def create_norm_vend(self):
		"""
		create the xml before vend
		"""
		try:
			root = etree.Element('ipayMsg', client=self.client, term=self.term, seqNum="0", time=str(self.today))
			elecMsg = etree.SubElement(root,'elecMsg', ver="2.44")
			vendReq = etree.SubElement(elecMsg, 'vendReq')
			ref = etree.SubElement(vendReq, 'ref')
			ref.text = str(self.my_ref)
			amt = etree.SubElement(vendReq, 'amt', cur="KES")
			amt.text = str(self.amount)
			numTokens = etree.SubElement(vendReq, 'numTokens')
			numTokens.text = "1"
			meter = etree.SubElement(vendReq, 'meter')
			meter.text = self.meter
			payType = etree.SubElement(vendReq, 'payType')
			payType.text = 'cash'
			params = etree.tostring(root, pretty_print=True, encoding='utf-8')
			return wrap(params)
		except Exception as e:
			return str(e)


	def create_reverse_vend(self, vend_time, ref):
		"""
		create the reverse vend
		"""
		try:
			root = etree.Element('ipayMsg', client=self.client, term=self.term, seqNum="2", time=str(self.today))
			elecMsg = etree.SubElement(root,'elecMsg', ver="2.44")
			vendRevReq = etree.SubElement(elecMsg, 'vendRevReq', repCount="1", origTime=str(vend_time))
			ref = etree.SubElement(vendRevReq, 'ref')
			ref.text = ref
			vendReq = etree.SubElement(elecMsg, 'vendReq')
			ref = etree.SubElement(vendReq, 'ref')
			ref.text = str(self.my_ref)
			amt = etree.SubElement(vendReq, 'amt', cur="KES")
			amt.text = str(self.amount)
			numTokens = etree.SubElement(vendReq, 'numTokens')
			numTokens.text = "1"
			meter = etree.SubElement(vendReq, 'meter')
			meter.text = self.meter
			payType = etree.SubElement(vendReq, 'payType')
			payType.text = 'cash'
			params = etree.tostring(root, pretty_print=True, encoding='utf-8')
			return wrap(params)
		except Exception as e:
			return str(e)

	def make_vend(self):
		"""
		make the vend request to the bizz switch server
		"""
		try:
			s = self.create_socket()
			data_frame = self.create_norm_vend()
			req = s.send(data_frame)
			print ("Request sent : %s" % time.ctime())
			time.sleep(5)
			resp = s.recv(2048)
			print ("Response received : %s" % time.ctime())
			data = un_wrap(resp)
			root = etree.fromstring(data)
			my_dict = {}
			for element in root.iter():
				if element.tag == 'ipayMsg':
					my_dict['vend_time'] = element.get('time')
				if element.tag == 'res':
					my_dict['code'] = element.get('code')
				if element.tag == 'ref':
					my_dict['reference'] = element.text
				if element.tag == 'util':
					my_dict['address'] = element.get('addr')
				if element.tag == 'stdToken':
					my_dict['token'] = element.text
					my_dict['units'] = element.get('units')
					my_dict['units_type'] = element.get('unitsType')
					my_dict['amount'] = element.get('amt')
					my_dict['tax'] = element.get('tax')
					my_dict['tarrif'] = element.get('tariff')
					my_dict['description'] = element.get('desc')
					my_dict['rct_num'] = element.get('rctNum')
				data = my_dict
			s.close()
			return data
		except Exception as e:
			return str(e)

	def make_reverse_vend(self):
		"""
		make the vend reversal request to the biz switch server
		"""
		try:
			s = self.create_socket()
			data_frame = self.create_reverse_vend(vend_time, ref)
			req = s.send(data_frame)
			time.sleep(5)
			resp = s.recv(2048)
			data = un_wrap(resp)
			root = etree.fromstring(data)
			my_dict = {}
			for element in root.iter():
				if element.tag == 'ipayMsg':
					my_dict['vend_rev_time'] = element.get('time')
				if element.tag == 'vendRevRes':
					if element.tag == 'ref':
						my_dict['ref'] = element.text
					if element.tag == 'res':
						my_dict['code'] = element.get('code')
				data = my_dict
			s.close()
			return data
		except Exception as e:
			return str(e)
