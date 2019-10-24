#!/usr/bin/env python
"""
signapp.py 
created by Rolly Maulana Awangga

"""
import random
import gspread
from oauth2client.service_account import  ServiceAccountCredentials
from Crypto.Cipher import AES
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

import config

class Kepo(object):
	def __init__(self):
		self.key = config.key
		self.iv = config.iv
		self.keyuri = "key"
		self.active_url8 = "https://cucunguk.herokuapp.com/" 
		self.active_url7 = "https://proyek3d4ti.herokuapp.com/"
		self.cdn8 = "https://raw.githubusercontent.com/D4TI/2018/master/kecil/"
		self.cdn7 = "https://raw.githubusercontent.com/D4TI/2017/master/kecil/"
		self.ekscdn = ".jpg"
		self.osjur = "https://raw.githubusercontent.com/himatifpoltekpos/sertifikat-morris-proyek/master/20"
		self.eksosjur = ".png"
		self.urlsiap = 'http://siap.poltekpos.ac.id/siap/besan.depan.php'
		self.urlkick='http://siap.poltekpos.ac.id/siap/besan.otorisasi.php?error=3'
		self.urllihatdata='http://siap.poltekpos.ac.id/siap/modul/simpati/index.php?mnux=master.mahasiswa.informasi&mdlid=62'
		self.urlsiappersonal = 'http://siap.poltekpos.ac.id/siap/modul/simpati/index.php?mnux=master.mahasiswa.informasi.detail&inqMhsw=inqMhswPribadi'
		self.urlubahdata='http://siap.poltekpos.ac.id/siap/modul/simpati/index.php?mnux=master.mahasiswa&mdlid=28'
		self.urlsiaportu = 'http://siap.poltekpos.ac.id/siap/modul/simpati/index.php?mnux=master.mahasiswa.edit&mhswedt=ortu'
		self.urllogout='http://siap.poltekpos.ac.id/siap/besan.otorisasi.php?logout=yes'
		self.matakuliah2 = {
		"kode":"TI43162",
		"semester" : "20182"
		}
		self.matakuliah3 = {
		"kode":"TI43233",
		"semester" : "20181"
		}
		self.apigithub = "https://api.github.com/repos/USERNAME/REPONAME/issues?sort=created&direction=desc"
		self.logname = 'datamahasiswa'
		self.client_secret = config.client_secret

	def insertLog(self,data):
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_dict(self.client_secret, scope)
		client = gspread.authorize(creds)
		self.sheet = client.open(self.logname).get_worksheet(1)
		return self.sheet.insert_row(data, 2)
		
	def random(self,ln):
		ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		chars=[]
		for i in range(ln):
			chars.append(random.choice(ALPHABET))
		return "".join(chars)

	def makeit16(self,uri):
		ln = len(uri)
		divln = ln // 16
		sp = (16+16*divln) - ln - len(str(ln))
		print(sp)
		if ln>9:
			dt = str(ln)+uri+self.random(sp)
		else:
			dt = "0"+str(ln)+uri+self.random(sp-1)
		return dt

	def generateURL(self, NPM, PASSWORD, PROYEK, NILAI, KET, Pembimbing):
		lengkap=self.sudahLengkap(NPM, PASSWORD, PROYEK, NILAI, KET, Pembimbing)
		data=self.getPersonalData(NPM,Pembimbing,100,KET)
		if lengkap:
			self.insertLog(data)
			active_url=self.getURL(PROYEK)
			uri=self.keyuri+NPM+'%'+NILAI+'%'+KET
			msg=self.makeit16(uri)
			obj=AES.new(self.key,AES.MODE_CBC,self.iv)
			cp = obj.encrypt(msg)
			return active_url+cp.hex()
		else:
			msg='Administrasi Kurang Lengkap'
			print(msg)
			return ''
	
	def sudahLengkap(self, NPM, PASSWORD, PROYEK, NILAI, KET, Pembimbing):
		adafoto=self.adaFoto(NPM,PROYEK)
		if not adafoto:
			print('Foto Diri Belum Pull Request')
		adaosjur=self.lulusOsjur(NPM)
		if not adaosjur:
			print('Sertifikat Morris Belum di Pull Request')
		print('Harap ditunggu, sedang dilakukan proses pengecekan nilai prasyarat.... (1-5 menit)')
		lulusmatakuliah=self.lulusMataKuliah(NPM,PASSWORD,PROYEK)
		if not lulusmatakuliah:
			print('Matakuliah prasyarat belum lulus')
		if adafoto and adaosjur and lulusmatakuliah:
			return True
		else:
			return False
	
	def getURL(self,PROYEK):
		if PROYEK == '2':
			active_url = self.active_url8
		else:
			active_url = self.active_url7
		return active_url
		
	def adaFoto(self,NPM, PROYEK):
		if PROYEK == '2':
			cdn = self.cdn8
		else:
			cdn = self.cdn7
		f = requests.get(cdn+NPM+self.ekscdn)
		if f.text[:3] == '404':
			res = False
		else:
			res = True
		return res

	def lulusOsjur(self,NPM):
		f = requests.get(self.osjur+NPM[1:3]+'/'+NPM+self.eksosjur)
		if f.text[:3] == '404':
			res = False
		else:
			res = True
		return res

	def lulusMataKuliah(self, NPM,password,PROYEK):
		if PROYEK == '2':
			matakuliah = self.matakuliah2
		else:
			matakuliah = self.matakuliah3
		self.openSiap()
		self.loginSiap(NPM,password)
		alllistnilai=self.getNilaiSemester(matakuliah['semester'])
		nilai=self.getNilaiMK(alllistnilai,matakuliah['kode'])
		print('Nilai : '+nilai)
		kelulusan = self.isLulus(nilai)
		return kelulusan
		
	def getPersonalData(self, NPM, Pembimbing,Nilai, Bimbingan):
		data=[]
		now = datetime.now()
		data.append(now.strftime("%d/%m/%Y %H:%M:%S"))
		data.append(NPM)
		data.append(self.getNamafromSiap())
		data.append(Pembimbing)
		data.append(self.getHPfromSiap())
		data.append(self.getNamaOrtufromSiap())
		data.append(self.getHPOrtufromSiap())
		data.append(Nilai)
		data.append(Bimbingan)
		self.closeSiap()
		return data
		
	def openSiap(self):
		options = Options()
		options.headless = True
		self.driver = webdriver.Chrome(options=options)
		self.driver.get(self.urlsiap)

	def loginSiap(self,NPM,password):
		self.driver.find_element_by_name('user_name').send_keys(NPM)
		self.driver.find_element_by_name('user_pass').send_keys(password)
		self.driver.find_element_by_name('login').click()
		success = False
		while success == False:
			try:
				siapnpm=self.driver.find_elements_by_class_name('cap-main')[7].text
				if siapnpm == NPM:
					status = True
				success = True
			except:
				if self.driver.current_url == self.urlkick:
					status = False
					success = True
		return status
	
	def openProfileSiap(self):
		success = False
		while success == False:
			try:
				self.driver.get(self.urllihatdata)
				self.driver.get(self.urlsiappersonal)
				success = True
			except:
				time.sleep(5)
		return success
	
	def getNamafromSiap(self):
		self.openProfileSiap()
		profile = self.driver.find_element_by_class_name('box').text
		nama=profile.splitlines()[1].split(' Nama ')[1]
		return nama
		
	def getHPfromSiap(self):
		self.openProfileSiap()
		profile = self.driver.find_elements_by_class_name('box')
		nohp=profile[3].text.splitlines()[10].split(', ')[2]
		return nohp
	
	def openProfileOrtuSiap(self):
		success = False
		while success == False:
			try:
				self.driver.get(self.urlubahdata)
				self.driver.get(self.urlsiaportu)
				success = True
			except:
				time.sleep(5)
		return success
	
	def getNamaOrtufromSiap(self):
		self.openProfileOrtuSiap()
		profile = self.driver.find_element_by_name('NamaAyah')
		namaayah=profile.get_attribute("value")
		profile = self.driver.find_element_by_name('NamaIbu')
		namaibu=profile.get_attribute("value")
		return 'Bpk. '+namaayah+' dan Ibu '+namaibu
		
	def getHPOrtufromSiap(self):
		self.openProfileOrtuSiap()
		profile = self.driver.find_element_by_name('HandphoneOrtu')
		nohp=profile.get_attribute("value")
		return nohp
	
	def getNilaiSemester(self,semester):
		#20182
		opsisemester="//option[@value='"+semester+"']"
		success = False
		count=0
		while success == False:
			try:
				#self.driver.find_element_by_link_text("Nilai Mahasiswa").click()
				self.driver.get("http://siap.poltekpos.ac.id/siap/modul/simpati/index.php?mnux=nilai.mahasiswa&mdlid=43")
				self.driver.find_element_by_xpath(opsisemester).click()
				self.driver.find_element_by_xpath("//input[@value='Cari' and @name='Cari']").click()
				tabel = self.driver.find_elements_by_xpath("//table[@class='box' and @align='left']/tbody/tr")
				daftar = []
				for i in tabel:
					string = i.text[2:10].strip()+","+i.text[-12:-11]
					daftar.append(string.split(','))
				daftar.remove(daftar[1])
				daftar.remove(daftar[0])
				success = True
			except:
				print('Data Tidak Ditemukan')
				time.sleep(5)
				count=count+1
				if count>5:
					success = True
					daftar=[]
		return daftar
		
	def getNilaiMK(self, daftar,MK):
		#kode_matkul = ['PPI1102', 'T4I222D4', 'TI43142']
		for i in daftar:
			if i[0] == MK:
				res = i[1]
		return res
	
	def isLulus(self, nilai):
		switcher= {
				"A": True,
				"B": True,
				"C": True,
				"D": True
				}
		return switcher.get(nilai, False)
	
	def closeSiap(self):
		self.driver.get(self.urllogout)
		while self.driver.current_url != self.urlsiap:
			time.sleep(1)
		self.driver.close()