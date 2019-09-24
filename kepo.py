#!/usr/bin/env python
"""
signapp.py 
created by Rolly Maulana Awangga

"""
import config
import random
from Crypto.Cipher import AES
import requests

class Kepo(object):
	def __init__(self):
		self.key = config.key
		self.iv = config.iv
		#self.active_url = config.active_url
		self.keyuri = config.keyuri

	def random(self,ln):
                ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                chars=[]
                for i in range(ln):
                        chars.append(random.choice(ALPHABET))
                return "".join(chars)

	def urlEncode16(self,uri):
		ln = len(uri)
		sp = 16 - ln - len(str(ln))
		if ln>9:
			dt = str(ln)+uri+self.random(sp)
		else:
			dt = "0"+str(ln)+uri+self.random(sp-1)
		return self.encodeData16(dt)

	def encodeData16(self,msg):
		obj=AES.new(self.key,AES.MODE_CBC,self.iv)
		cp = obj.encrypt(msg)
		return cp.hex()
    
	def generateURL(self,NPM):
		if NPM[2:3] == '8':
			active_url = config.active_url8
		else:
			active_url = config.active_url7
		return active_url+self.urlEncode16(self.keyuri+NPM)
		
	def adaFoto(self,NPM):
		if NPM[2:3] == '8':
			cdn = config.cdn8
		else:
			cdn = config.cdn7
		f = requests.get(cdn+NPM+'.jpg')
		if f.text[:3] == '404':
			res = False
		else:
			res = True
		return res

