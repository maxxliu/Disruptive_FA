from .models import *
from django.utils import timezone
import data_gathering

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
	
	mid = []
	for obj in pre:
		current = Summary_Data.objects.get(ticker = obj)
		# if 0.5*summary.market_cap <= current.market_cap <= 1.5*summary.market_cap:
		diff = abs(current.market_cap - summary.market_cap)			
		if current.ticker.ticker != stock.ticker:
			if '&#39;' in current.ticker.name:
				name = current.ticker.name.replace('&#39;', "'")
				mid.append([current.ticker.ticker, name, diff])
			else:
				mid.append([current.ticker.ticker, current.ticker.name, diff])

	recommended = []
	if len(mid) == 5:
		for item in mid:
			recommended.append([item[0], item[1]])
		
		return recommended

	elif len(mid) > 5:
		sorted_mid = sorted(mid, key=lambda x: x[2])
		for i in range(5):
			recommended.append(sorted_mid[i])

		return recommended

	else:
		for item in mid:
			recommended.append([item[0], item[1]])
		
		pre2 = Stock.objects.filter(sector = stock.sector)

		mid2 = []
		for obj in pre2:
			current = Summary_Data.objects.get(ticker = obj)
			if 0.25*summary.market_cap <= current.market_cap <= 1.75*summary.market_cap:
				diff = abs(current.market_cap - summary.market_cap)			
				if current.ticker.ticker != stock.ticker:
					if '&#39;' in current.ticker.name:
						name = current.ticker.name.replace('&#39;', "'")
						mid2.append([current.ticker.ticker, name, diff])
					else:
						mid2.append([current.ticker.ticker, current.ticker.name, diff])

		sorted_mid2 = sorted(mid2, key=lambda x: x[2])
		for i in range(5 - len(mid)):
			recommended.append(sorted_mid2[i])

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
	pre3 = []
	pre.append(stock.ticker + ' | ')
	if '&#39;' in stock.name:
		name = stock.name.replace('&#39;', "'")
		pre.append(name + ' | ')
	else:
		pre.append(stock.name + ' | ')
	pre.append('Previous Close: $' + str(summary.previous_close))
	pre2.append('High: $' + str(summary.year_high) + ' | ')
	pre2.append('Low: $' + str(summary.year_low) + ' | ')
	pre2.append('Beta: ' + str(summary.beta) + ' | ')
	pre2.append('Market Cap: $' + str(summary.market_cap))
	pre3.append(str(stock.sector) + ' | ')
	pre3.append(str(stock.industry))

	header_list = [''.join(pre), ''.join(pre2), ''.join(pre3)]

	return header_list


def format_dates(data_date):
	'''
	Formats the dates list to use in the financials table header with a 
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

def format_fin_statements(fin_statements):
	'''
	formats the fin statement list to use in the financials table with a 
	list of fin_statement objects

	Inputs:
		fin_statements: a list of fin_statement objects

	Outputs:
		fin_table_list: list of fin_statement values to use in the financials 
		table
	'''
	fin_table_list = []
	for obj in fin_statements:
		row = [obj.line_item, obj.year_1_val, obj.year_2_val, obj.year_3_val, 
			obj.year_4_val]
		fin_table_list.append(row)

	return fin_table_list


def advanced_search(sect, indust, mc):
	'''
	'''
	mc_dict = {
		"0": (0, 1000000),
		"1M": (1000000, 100000000),
		"100M": (100000000, 1000000000),
		"1B": (1000000000, 10000000000),
		"10B": (0, 0)}

	if sect != "None" and indust != "None":
		pre = Stock.objects.filter(sector = sect, industry = indust)
		
		if mc != "None":
			mid = []
			for obj in pre:
				current = Summary_Data.objects.get(ticker = obj)
				if mc != "10B":
					if mc_dict[mc][0] < current.market_cap <= mc_dict[mc][1]:
						mid.append(obj)
				else:
					if current.market_cap > 10000000000:
						mid.append(obj)
			fin = []
			for obj in mid:
				fin.append([obj.ticker, obj.name])

			return fin

		else:
			fin = []
			for obj in pre:
				fin.append([obj.ticker, obj.name])

			return fin

	elif sect != "None" and indust == "None":
		pre = Stock.objects.filter(sector = sect)
		if mc != "None":
			mid = []
			for obj in pre:
				current = Summary_Data.objects.get(ticker = obj)
				if mc != "10B":
					if mc_dict[mc][0] < current.market_cap <=mc_dict[mc][1]:
						mid.append(obj)
				else:
					if current.market_cap > 10000000000:
						mid.append(obj)
			fin = []
			for obj in mid:
				fin.append([obj.ticker, obj.name])

			return fin

		else:
			fin = []
			for obj in pre:
				fin.append([obj.ticker, obj.name])

			return fin

	else:
		if mc != "10B":
			pre = Summary_Data.objects.filter(mc_dict[mc][0] < market_cap <= mc_dict[mc][1])

			fin = []
			for obj in pre:
				fin.append([obj.ticker.ticker, obj.ticker.name])

			return fin

		else:
			pre = Summary_Data.objects.filter(market_cap > 10000000000)

			fin = []
			for obj in pre:
				fin.append([obj.ticker.ticker, obj.ticker.name])

			return fin


def update_summary_data(stock_ticker):
	'''
	updates summary data for stocks
	'''
    stock_ticker = stock_ticker.upper()
    try:
        s = Stock.objects.get(ticker=stock_ticker)
        sd = Summary_Data.objects.get(ticker=s)
    except:
        return None
    if sd.updated.day != timezone.now().day:
        new_sd = data_gathering.summary_info(stock_ticker)
        fix_summary(new_sd)
        sd.target = float(new_sd['1 Year Target'])
        sd.year_high = float(new_sd['52 Week High/Low'][0])
        sd.year_low = float(new_sd['52 Week High/Low'][1])
        sd.beta = float(new_sd['Beta'])
        sd.market_cap = new_sd['Market cap']
        sd.previous_close = float(new_sd['Previous Close'])
        sd.updated = timezone.now()
        sd.save()


def fix_summary(summ_d):
	'''
	fixes the summary dictionary if its formatting is inconsistent
	'''
    for key, value in summ_d.items():
        if value == '':
            summ_d[key] = 0

    for key in ['1 Year Target', '52 Week High/Low', 'Beta', 'Market cap', 'Previous Close']:
        if key in summ_d:
            if key != '52 Week High/Low':
                if type(summ_d[key]) == list:
                    summ_d[key] = 0
            else:
                try:
                    summ_d[key][0] = float(summ_d[key][0])
                except:
                    summ_d[key] = [0, 0]
        else:
            if key == '52 Week High/Low':
                summ_d[key] = [0, 0]
            else:
                summ_d[key] = 0