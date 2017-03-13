from __future__ import unicode_literals

from django.db import models

# Create your models here.
class rm(models.Model):
	'''
	Class for risk object table in the Django ORD

	Attributes:
		rm_id: id of the risk object
		risk: risk score associated with risk object
	'''
	rm_id = models.IntegerField()
	risk = models.DecimalField(max_digits=6, decimal_places=5)