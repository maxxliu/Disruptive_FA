from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Stock(models.Model):
	'''
	Class for the stock table in the Django ORD
	
	Attributes:
		ticker: stock ticker
		name: name of the company
		sector: company sector
		industry: company industry

	'''
	ticker = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	sector = models.CharField(max_length=200)
	industry = models.CharField(max_length=200)

	def __str__(self):
		return self.ticker


class Fin_Statement(models.Model):
	'''
	Class for the financial statements table for stocks in the Django ORD

	Attributes:
		ticker: a stock object
		statement_type: financial statement type
		line_item: line item type
		year_1_val: value of financial statement in year 1
		year_2_val: value of financial statement in year 2
		year_3_val: value of financial statement in year 3
		year_4_val: value of financial statement in year 4
	'''
	ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
	statement_type = models.CharField(max_length=200)
	line_item = models.CharField(max_length=200)
	year_1_val = models.BigIntegerField()
	year_2_val = models.BigIntegerField()
	year_3_val = models.BigIntegerField()
	year_4_val = models.BigIntegerField()

	def __str__(self):
		return self.ticker.ticker

class Data_Date(models.Model):
	'''
	Class for the data dates table for a stock in the Django ORD

	Attributes:
		ticker: a stock object
		year_1: date the year_1_val financial value was last updated
		year_2: date the year_2_val financial value was last updated
		year_3: date the year_3_val financial value was last updated
		year_4: date the year_4_val financial value was last updated
	'''
	ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
	year_1 = models.CharField(max_length=200)
	year_2 = models.CharField(max_length=200)
	year_3 = models.CharField(max_length=200)
	year_4 = models.CharField(max_length=200)

	def __str__(self):
		return self.ticker.ticker


class Summary_Data(models.Model):
	'''
	Class for the summary data table for a stock in the Django ORD

	Attributes:
		ticker: a stock object
		target: target for stock
		year_high: year high's stock price
		Year_low: year low's stock price
		market_cap: the current day's market cap
		previous_close: the stocks previous close price
		updated: time this data was last updated
	'''
	ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
	target = models.DecimalField(max_digits=10, decimal_places=2)
	year_high = models.DecimalField(max_digits=10, decimal_places=2)
	year_low = models.DecimalField(max_digits=10, decimal_places=2)
	beta = models.DecimalField(max_digits=5, decimal_places=2)
	market_cap = models.BigIntegerField()
	previous_close = models.DecimalField(max_digits=10, decimal_places=2)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.ticker.ticker