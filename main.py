#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 20:54:32 2019

@author: awangga
"""

import kepo
import qrcode
import requests

cdn="https://raw.githubusercontent.com/D4TI/2018/master/kecil/"


kepo = kepo.Kepo()
print("NPM : ")
NPM=input()

f = requests.get(cdn+NPM+'.jpg')
if f.text[:3] == '404':
	print("Upload Foto Dulu Coy")
else:
	crot=kepo.generateURL(NPM)
	img = qrcode.make(crot)
	img.save(NPM+".png")
	print("File QrCode Telah Dibuat")