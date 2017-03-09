from django.shortcuts import render, HttpResponse
from django.forms.models import model_to_dict
from .models import *
from .helper import *
from .dcf_equation import *
from risk_survey.models import *
from .get_lsts import SECTORS, INDUSTRY
from django.core.exceptions import *

# Create your views here.
def index(request):
	return render(request, 'quick_search/stock_search.html', 
		{'sector': SECTORS,
		'industry': INDUSTRY})


def results(request):
	if request.method == "POST":
		search = request.POST['textfield'].upper()
	elif request.method == "GET":
		search = request.GET['textfield']

	if search:
		try:
			stock = Stock.objects.get(ticker = search)
			update_summary_data(stock.ticker)

			try:
				summary_data = Summary_Data.objects.get(ticker = stock)
				header_list = format_header(stock, summary_data)

				recommended = get_recommended(stock, summary_data)

			except Summary_Data.DoesNotExist:
				return render(request, 'quick_search/error.html')

			try:
				data_date = Data_Date.objects.get(ticker = stock)
				date_list = format_dates(data_date)
				# check for update on fin statemenet values

				fin_statements = Fin_Statement.objects.filter(ticker = stock)
				fin_table_list = format_fin_statements(fin_statements)

				dcf_dict = create_dict(stock.ticker)
				r_m = float(str(rm.objects.get(rm_id = 1).risk))
				price, growth, years = dcf_calculator(dcf_dict, r_m)

			except Data_Date.DoesNotExist:
				return render(request, 'quick_search/results.html',
					{'header': header_list,
					'dates': ['n/a', 'n/a', 'n/a', 'n/a'],
					'fin_statements': [['n/a', 'n/a', 'n/a', 'n/a', 'n/a']],
					'error': ["Sorry, it seems like we don't have enough information for this stock. Please take a look at our list of recommended stocks."],
					'dcf': [],
					'recommended': recommended})

			return render(request, 'quick_search/results.html', 
				{'header': header_list,
				'dates': date_list,
				'fin_statements': fin_table_list,
				'error': [],
				'dcf': ['$' + str(round(price, 2))],
				'recommended': recommended
				})		
		except Stock.DoesNotExist:
			return render(request, 'quick_search/error.html')
	else:
		return render(request, 'quick_search/stock_search.html', 
		{'sector': SECTORS,
		'industry': INDUSTRY})


def advanced(request):
	if request.method == "POST":			
		sect = request.POST['Sector']
		indust = request.POST['Industry']
		mc = request.POST['Market Cap']

		fin = advanced_search(sect, indust, mc)

		if fin == ["None"]:
			return render(request, 'quick_search/stock_search.html', 
				{'sector': SECTORS,
				'industry': INDUSTRY})
			

		elif not fin:
			return render(request, 'quick_search/error.html')

		else:
			return render(request, 'quick_search/advanced.html',
				{'recommended': fin})