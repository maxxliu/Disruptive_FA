from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Stock(models.Model):
	ticker = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	sector = models.CharField(max_length=200)
	industry = models.CharField(max_length=200)

	def __str__(self):
		return self.ticker, self.name, self.sector, self. industry


class Fin_Statements(models.Model):
	ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
	statement_type = models.CharField(max_length=200)
	line_item = models.CharField(max_length=200)
	year_1_val = models.BigIntegerField()
	year_2_val = models.BigIntegerField()
	year_3_val = models.BigIntegerField()
	year_4_val = models.BigIntegerField()

	def __str__(self):
		return self.ticker, self.statement_type, self.line_item, self.year_1_val, self.year_2_val, self.year_3_val, self.year_4_val


class Data_Dates(models.Model):
	ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
	year_1 = models.CharField(max_length=200)
	year_2 = models.CharField(max_length=200)
	year_3 = models.CharField(max_length=200)
	year_4 = models.CharField(max_length=200)

	def __str__(self):
		return self.ticker, self.year_1, self.year_2, self.year_3, self.year_4


class Summary_Data(models.Model):
	ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
	target = models.DecimalField(max_digits=7, decimal_places=2)
	year_high = models.DecimalField(max_digits=7, decimal_places=2)
	year_low = models.DecimalField(max_digits=7, decimal_places=2)
	beta = models.DecimalField(max_digits=5, decimal_places=2)
	market_cap = models.BigIntegerField()
	previous_close = models.DecimalField(max_digits=7, decimal_places=2)