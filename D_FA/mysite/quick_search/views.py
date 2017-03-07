from django.shortcuts import render, HttpResponse
from django.forms.models import model_to_dict
from .models import *
from .helper import *
from django.core.exceptions import *

# Create your views here.
def index(request):
	return render(request, 'quick_search/quick_search.html')


def results(request):
	if request.method == "POST":
		search = request.POST['textfield']
	elif request.method == "GET":
		search = request.GET['textfield']

	if search:
		try:
			stock = Stock.objects.get(ticker = search)
			# format render dict entry for stock

			summary_data = Summary_Data.objects.get(ticker = stock)
			header_list = format_header(stock, summary_data)
			# check for update on summary data values
			# format render dict entry for summary data

			data_date = Data_Date.objects.get(ticker = stock)
			date_list = format_dates(data_date)
			# check for update on fin statemenet values

			fin_statements = Fin_Statement.objects.filter(ticker = stock)
			# calculate DCF and rating from financials list
			# format render dict entry for financials

			recommended = get_recommended(stock, summary_data)

			return render(request, 'quick_search/results.html', 
				{'header': header_list,
				'dates': date_list,
				'recommended': recommended
				})		
		except Stock.DoesNotExist:
			return HttpResponse("<p>error</p>")
	else:
		return render(request, 'quick_search/quick_search.html')