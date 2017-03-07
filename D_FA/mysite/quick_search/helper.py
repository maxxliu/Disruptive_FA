from .models import *

# Helper functions for the quick_search views.py

def get_recommended(stock, summary):
	'''
	Gets a list of stocks that have the same sector and industry as the 
	queried stock with a similar market cap

	Inputs:
		stock: the queried stock object
		summary: the queried summary_data object

	Outpus:
		recommended: a list of recommended stock objects
	'''
	pre = Stock.objects.filter(sector = stock.sector, 
		industry = stock.industry)
	
	recommended = []
	for obj in pre:
		current = Summary_Data.objects.get(ticker = obj)
		if 0.8*summary.market_cap <= current.market_cap \
		<= 1.2*summary.market_cap:
			if current.ticker.ticker != stock.ticker:
				recommended.append(current.ticker.ticker)

	return recommended


def format_header(stock, summary):
	'''
	Formats the header list of the results page with a stock and summary_data 
	object

	Inputs:
		stock: the queried stock object
		summary: the queried summary_data object

	Outputs:
		header_list: list of tuples for render dictionary
	'''
	pre = []
	pre2 = []
	pre.append(stock.ticker + ' | ')
	pre.append(stock.name + ' | ')
	pre.append('Previous Close: $' + str(summary.previous_close))
	pre2.append('High: $' + str(summary.year_high) + ' | ')
	pre2.append('Low: $' + str(summary.year_low) + ' | ')
	pre2.append('Beta: ' + str(summary.beta) + ' | ')
	pre2.append('Market Cap: $' + str(summary.market_cap))

	header_list = [''.join(pre), ''.join(pre2)]

	return header_list


def format_dates(data_date):
	'''
	Formates the dates list to use in the financials table header with a 
	data_date object

	Inputs:
		data_date: the queried data_date object

	Outputs:
		date_list: list of dates to use in the financials table header
	'''
	date_list = []
	date_list.append(data_date.year_1)
	date_list.append(data_date.year_2)
	date_list.append(data_date.year_3)
	date_list.append(data_date.year_4)

	return date_list
