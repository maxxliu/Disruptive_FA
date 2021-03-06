from django.shortcuts import render, HttpResponse
from django.forms.models import model_to_dict
from .models import *
from .helper import *
from .dcf_equation import *
from risk_survey.models import *
from decimal import *
from .get_lsts import SECTORS, INDUSTRY
from django.core.exceptions import *

# Create your views here.
def index(request):
	'''
	Function to render the index stock search page

	Inputs:
		request: a request to the page

	Returns:
		render: html template of the stock search page with sector and 
		industry lists stored in a dictionary
	'''
	return render(request, 'quick_search/stock_search.html', 
		{'sector': SECTORS,
		'industry': INDUSTRY})


def results(request):
	'''
	Function to render the search results page of the stock search app

	Inputs:
		request: either get or post which is a stock ticker

	Results:
		render: html template of the results page with stock parameters stored 
		in a dictionary
	'''
	if request.method == "POST":
		search = request.POST['textfield'].upper()
	elif request.method == "GET":
		search = request.GET['textfield']

	if search == "DFA":
		return render(request, 'quick_search/dfa.html')
	elif search:
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

				fin_statements = Fin_Statement.objects.filter(ticker = stock)
				fin_table_list = format_fin_statements(fin_statements)

				dcf_dict = create_dict(stock.ticker)
				r_m = float(str(rm.objects.get(rm_id = 1).risk))
				price, growth, years, inaccurate, rating = \
					dcf_calculator(dcf_dict, r_m)

				if not inaccurate:				
					if round(price, 2) < 0:
						price = '-$' + str(abs(round(price, 2)))
					else:
						price = '$' + str(round(price, 2))

			except Data_Date.DoesNotExist:
				return render(request, 'quick_search/results.html',
					{'header': header_list,
					'dates': ['n/a', 'n/a', 'n/a', 'n/a'],
					'fin_statements': [['n/a', 'n/a', 'n/a', 'n/a', 'n/a']],
					'error': ["Sorry, it seems like we don't have enough" + 
						" information for this stock. Please take a look at" + 
						" our list of recommended stocks."],
					'dcf': [],
					'recommended': recommended})

			return render(request, 'quick_search/results.html', 
				{'header': header_list,
				'dates': date_list,
				'fin_statements': fin_table_list,
				'error': [],
				'dcf': [price, inaccurate, rating],
				'recommended': recommended})

		except Stock.DoesNotExist:
			return render(request, 'quick_search/error.html')
	else:
		return render(request, 'quick_search/stock_search.html', 
		{'sector': SECTORS,
		'industry': INDUSTRY})


def advanced(request):
	'''
	Function to render the advanced search results page

	Inputs:
		request: a post request that specifies queries sector, industry, or 
		market cap

	Returns:
		render: html template of the advanced search page with the list of 
		recommended stocks stored in a dictionary
	'''
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


def thanks(request):
	'''
	Function to render the thanks page after agreeing/disagreeing with our 
	stock rating and also updates the users rm score

	Inputs:
		request: a post request that specifies whether the user agrees/
		diasgrees with our rating

	Returns:
		render: html template of the thanks page
	'''
	if request.method == "POST":
		agree = Decimal(request.POST['agree'])
		r_m = rm.objects.get(rm_id = 1)
		r_m.risk += agree
		r_m.save()

		return render(request, 'quick_search/thanks.html')