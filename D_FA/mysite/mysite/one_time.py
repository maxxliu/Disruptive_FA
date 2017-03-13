# function to reset risk score on initializing site

from risk_survey.models import *

def starter():
	'''
	Resets teh risk score object to default value of 0.095
	'''
	obj = rm.objects.get(rm_id = 1)
	obj.risk = 0.095
	obj.save()