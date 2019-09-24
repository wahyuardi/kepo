#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 20:54:32 2019

@author: awangga
"""

import kepo
import qrcode


kepo = kepo.Kepo()
print("NPM : ")
NPM=input()
if kepo.adaFoto(NPM):
	crot=kepo.generateURL(NPM)
	img = qrcode.make(crot)
	img.save("./"+NPM+".png")
	print("File QrCode Telah Dibuat")
else:
	print("Upload Foto Dulu Coy")