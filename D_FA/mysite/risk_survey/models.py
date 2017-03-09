from __future__ import unicode_literals

from django.db import models

# Create your models here.
class rm(models.Model):
	rm_id = models.IntegerField()
	risk = models.DecimalField(max_digits=6, decimal_places=5)