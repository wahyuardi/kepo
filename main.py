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

crot=kepo.generateURL(NPM)

img = qrcode.make(crot)
img.save("NPM.jpg")
print("File QrCode Telah Dibuat")