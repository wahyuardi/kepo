#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 20:54:32 2019

@author: awangga
"""

import kepo
import qrcode
#import getpass


saya = kepo.Kepo()
print("NPM : ")
NPM=input()
print("Proyek : ")
PROYEK=input()
print("Password SIAP : ")
PASSWORD=input()
#PASSWORD = getpass.getpass('Password SIAP : ')
print("Kode DOSEN : ")
Pembimbing=input()
print("Progres yang dilaporkan : ")
Bimbingan=input()
print("Nilai : ")
Nilai=input()
print("masukkan data github.com/userrepo/namarepo")
print("User Repo : ")
userrepo=input()
print("Nama Repo : ")
namarepo=input()
print("pertemuan ke : ")
pertemuan=input()


crot=saya.generateURL(NPM, PASSWORD, PROYEK, Nilai, Bimbingan, Pembimbing,userrepo,namarepo,pertemuan)
if crot != '':
	img = qrcode.make(crot)
	img.save("./"+NPM+".png")
	print("File QrCode Telah Dibuat")
