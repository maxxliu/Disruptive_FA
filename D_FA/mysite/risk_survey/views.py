from django.shortcuts import render, HttpResponse
from .survey import *
from decimal import *
from risk_survey.models import *

# Create your views here.
def index(request):
	question_list = get_questions()

	return render(request, 'risk_survey/risk_survey.html',
		{'questions': question_list})


def scored(request):
	if request.method == "POST":
		answer_list = [request.POST['Question 0'], 
			request.POST['Question 1'], 
			request.POST['Question 2'], 
			request.POST['Question 3'], 
			request.POST['Question 4']]

		adjust = Decimal('0')
		for answer in answer_list:
			adjust += Decimal(answer)

		obj = rm.objects.get(rm_id = 1)
		obj.risk += adjust
		obj.save()

	return render(request, 'risk_survey/scored.html',
		{'scores': answer_list})


def reset(request):
	if request.method == "POST":
		obj = rm.objects.get(rm_id = 1)
		obj.risk = Decimal(0.095)
		obj.save()

	return render(request, 'risk_survey/reset.html')