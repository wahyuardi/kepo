#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 20:54:32 2019

@author: awangga
"""

import kepo
import qrcode


saya = kepo.Kepo()
print("NPM : ")
NPM=input()
print("Proyek : ")
PROYEK=input()
print("Password SIAP : ")
PASSWORD=input()
print("Kode Calon Pembimbing/Pembimbing : ")
Pembimbing=input()
print("Progres yang dilaporkan : ")
Bimbingan=input()
print("Nilai : ")
Nilai=input()


crot=saya.generateURL(NPM, PASSWORD, PROYEK, Nilai, Bimbingan, Pembimbing)
if crot != '':
	img = qrcode.make(crot)
	img.save("./"+NPM+".png")
	print("File QrCode Telah Dibuat")
