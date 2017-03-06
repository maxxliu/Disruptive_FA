from .models import *

# Helper functions for the quick_search views.py

def get_recommended(stock, summary):
	'''
	Gets a list of stocks that have the same sector and industry as the 
	queried stock with a similar market cap

	Inputs:
		stock: the queried stock object
		summary: the queried summary object

	Outpus:
		recommended: a list of recommended stock objects
	'''
	pre = Stock.objects.filter(sector = stock.sector, industry = stock.industry)
	
	recommended = []
	for obj in pre:
		current = Summary_Data.objects.get(ticker = obj)
		if 0.8*summary.market_cap <= current.market_cap <= 1.2*summary.market_cap:
			if current.ticker.ticker != stock.ticker:
				recommended.append(current.ticker.ticker)

	return recommended