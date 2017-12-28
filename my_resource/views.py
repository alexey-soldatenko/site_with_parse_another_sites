from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
from my_resource.models import Parse_result
from datetime import datetime

# Create your views here.
def main(request):
	if request.method == 'GET':
		return render(request, 'main.html')
	
	#периодический ajax-запрос	
	elif request.method == 'POST' and request.is_ajax():
		#получаем последнюю дату обновления у клиента
		date = request.POST['last_date']

		if date == 'undefined' or date == '':
			try:
				date = Parse_result.objects.latest('date').date
				date = date.strftime('%d.%m.%Y %H:%M:%S.%f')
			except:
				return HttpResponse('')

		old_date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S.%f')
		#получаем последнюю дату обновления в базе данных
		new_date = Parse_result.objects.latest('date').date
		new_date = new_date.strftime('%d.%m.%Y %H:%M:%S.%f')

		#извлекаем записи, сделанные позже последнего обновления у клиента
		all_new_result = Parse_result.objects.filter(date__gt = old_date).order_by('-date')

		#преобразуем данные в требуемый текст
		block1 = render_to_string('message_block1.html', {'parse_url': all_new_result})
		block2 = render_to_string('message_block2.html',  {'parse_url': all_new_result})
		data = {'new_date':new_date, 'block1': block1, 'block2':block2}
		#отправляем json-ответ
		answer = json.dumps(data)
		return HttpResponse(answer)

def take_last_date(request):
	if request.method == 'POST' and request.is_ajax():
		try:
			#получаем последнюю дату обновления в базе данных
			new_date = Parse_result.objects.latest('date').date
			date = new_date.strftime('%d.%m.%Y %H:%M:%S.%f')
			return HttpResponse(date)
		except Exception as err:
			return HttpResponse('')

