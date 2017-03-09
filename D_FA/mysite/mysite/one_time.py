from risk_survey.models import *

def starter():
	obj = rm.objects.get(rm_id = 1)
	obj.risk = 0.095
	obj.save()