from django.core.management.base import BaseCommand, CommandError
from my_resource.models import URL_Parse, Parse_result

import threading
from urllib import request
from lxml import html 
import re



class MyThreadTimer:
	def __init__(self, url, timeshift):
		self.url = url
		self.timeshift = timeshift
		#блокировщик
		self.lock = threading.Lock()

	def run(self):
		try:
			#открываем url
			response = request.urlopen(self.url)
		except:
			#атомарное выполнение операций
			self.lock.acquire()
			#заносим результаты в базу данных
			new_result, created = Parse_result.objects.get_or_create(url = self.url)
			new_result.text_encode = ''
			new_result.title = ''
			new_result.h1 = ''
			new_result.status = False
			new_result.save()
			self.lock.release()
		else:
			#выполняем парсинг полученного результата
			headers = response.info()
			try:
				text_encode = re.findall(r'charset=([\w,\-]+)', headers['Content-Type'])[0]
				data = response.read().decode(text_encode)
			except IndexError:
				text_encode = ''
				#кодировка по умолчанию utf-8
				data = response.read().decode('utf-8')
			document = html.fromstring(data)
			#находим заголовок страницы
			try:
				title = document.find('.//title').text
			except:
				title = ''
			body = document.find('body')
			try:
				#находим h1 страницы
				h1 = body.find('.//h1').text 
			except:
				h1 = ''
			#атомарное выполнение операций
			self.lock.acquire()
			#заносим результаты в базу данных
			new_result, created = Parse_result.objects.get_or_create(url = self.url)
			new_result.text_encode = text_encode
			new_result.title = title
			new_result.h1 = h1
			new_result.status = True 
			new_result.save()
			self.lock.release()
		
		self.start()

	def start(self):
		#запускаем таймер
		thread = threading.Timer(self.timeshift, self.run)
		thread.start()



class Command(BaseCommand):
	help = 'Обработка URL базы данных'

	def handle(self, *args, **kwargs):
		''' запускаем отдельный поток-таймер для оброботки каждого url в базе данных'''
		all_url = URL_Parse.objects.all()
		for url in all_url:
			#временной интервал для периодической обработки url
			timeshift = url.minute*60 + url.second
			thread = MyThreadTimer(url.url, timeshift)
			thread.start()


