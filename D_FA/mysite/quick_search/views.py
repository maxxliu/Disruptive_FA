from django.shortcuts import render, HttpResponse
from .models import *
from django.core.exceptions import *

# Create your views here.
def index(request):
	return render(request, 'quick_search/quick_search.html')


def results(request):
	if request.method == "POST":
		search = request.POST['textfield']
		try:
			stock = Stock.objects.get(ticker = search)
			fin_statement = Fin_Statement.objects.get(ticker = stock)
			data_date = Data_Date.objects.get(ticker = stock)
			summary_data = Summary_Data.objects.get(ticker = stock)
			
			# check for updates on fin_statement and summary_data
			# use financials to calculate DCF and Buy/Sell/Hold rating
			# format render dictionary

			return render(request, 'quick_search/results.html', {'stock': [stock.ticker, stock.name],
				'fin_statement': [fin_statement.statement_type],
				'summary_data': [summary_data.updated, summary_data.previous_close]})		
		except Stock.DoesNotExist:
			return HttpResponse("<p>error</p>")
	else:
		return render(request, 'quick_search/quick_search.html')
