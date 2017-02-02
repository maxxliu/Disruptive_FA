# Financial Statement Data Scraping
# Max Liu


import bs4
import requests


'''
example data structure for holding financial data

data = {"Period Ending": []
		"Income Statement": {"Total Revenue": []
								"Cost of Revenue": []
		}
		"Balance Sheet": {}
		"Cash Flow": {}
		}
'''


def collect_data(ticker):
	'''
	takes a ticker and collect financial data relating to the ticker
	'''
	pass