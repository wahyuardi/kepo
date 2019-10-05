#!/usr/bin/env python
"""
signapp.py 
created by Rolly Maulana Awangga

"""
import random
from Crypto.Cipher import AES
import requests

class Kepo(object):
	def __init__(self):
		self.key = "rollysuprganteng"
		self.iv = "1234surabihaneut"
		self.keyuri = "key"
		self.active_url8 = "https://cucunguk.herokuapp.com/" 
		self.active_url7 = "https://proyek3d4ti.herokuapp.com/"
		self.cdn8 = "https://raw.githubusercontent.com/D4TI/2018/master/kecil/"
		self.cdn7 = "https://raw.githubusercontent.com/D4TI/2017/master/kecil/"

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
    
	def generateURL(self,NPM, PROYEK):
		if PROYEK == '2':
			active_url = self.active_url8
		else:
			active_url = self.active_url7
		return active_url+self.urlEncode16(self.keyuri+NPM)
		
	def adaFoto(self,NPM, PROYEK):
		if PROYEK == '2':
			cdn = self.cdn8
		else:
			cdn = self.cdn7
		f = requests.get(cdn+NPM+'.jpg')
		if f.text[:3] == '404':
			res = False
		else:
			res = True
		return res

