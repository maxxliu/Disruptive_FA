from django.shortcuts import render, HttpResponse
from .survey import *

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

	return render(request, 'risk_survey/scored.html',
		{'scores': answer_list})