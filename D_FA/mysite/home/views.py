from django.shortcuts import render
from .get_lsts import SECTORS, INDUSTRY
from .survey import *

# Create your views here.
def index(request):
	'''
	Function to render the index page

	Inputs:
		request: a request to the page

	Returns:
		render: html template of the home page
	'''
	return render(request, 'home/home.html')


def stock_search(request):
	'''
	Function to render the index stock search page

	Inputs:
		request: a request to the stock search page

	Returns:
		render: html template of the stock search page with sector and 
		industry lists stored in a dictionary
	'''
	return render(request, 'quick_search/stock_search.html', 
		{'sector': SECTORS,
		'industry': INDUSTRY})


def risk_survey(request):
	'''
	Function to render the index risk survey page

	Inputs:
		request: a request to the risk survey page

	Returns:
		render: html template of the risk survey page with a questions 
		list stored in a dictionary
	'''
	question_list = get_questions()

	return render(request, 'risk_survey/risk_survey.html',
		{'questions': question_list})


def info(request):
	'''
	Function to render the info page of "Behind the Calculations"

	Inputs:
		request: a request to "Behind the Calculations"

	Returns:
		render: html template of the info page
	'''
	return render(request, 'home/info.html')


def step_1(request):
	'''
	Function to render the step_1 page of "Behind the Calculations"

	Inputs:
		request: a request to step_1 of "Behind the Calculations"

	Returns:
		render: html template of the step_1 page
	'''
	return render(request, 'home/step_1.html')


def step_2(request):
	'''
	Function to render the step_2 page of "Behind the Calculations"

	Inputs:
		request: a request to step_2 of "Behind the Calculations"

	Returns:
		render: html template of the step_2 page
	'''
	return render(request, 'home/step_2.html')


def step_3(request):
	'''
	Function to render the step_3 page of "Behind the Calculations"

	Inputs:
		request: a request to step_3 of "Behind the Calculations"

	Returns:
		render: html template of the step_3 page
	'''
	return render(request, 'home/step_3.html')


def step_4(request):
	'''
	Function to render the step_4 page of "Behind the Calculations"

	Inputs:
		request: a request to step_4 of "Behind the Calculations"

	Returns:
		render: html template of the step_4 page
	'''
	return render(request, 'home/step_4.html')


def step_5(request):
	'''
	Function to render the step_5 page of "Behind the Calculations"

	Inputs:
		request: a request to step_5 of "Behind the Calculations"

	Returns:
		render: html template of the step_5 page
	'''
	return render(request, 'home/step_5.html')


def step_6(request):
	'''
	Function to render the step_6 page of "Behind the Calculations"

	Inputs:
		request: a request to step_6 of "Behind the Calculations"

	Returns:
		render: html template of the step_6 page
	'''
	return render(request, 'home/step_6.html')


def step_7(request):
	'''
	Function to render the step_7 page of "Behind the Calculations"

	Inputs:
		request: a request to step_7 of "Behind the Calculations"

	Returns:
		render: html template of the step_7 page
	'''
	return render(request, 'home/step_7.html')


def step_8(request):
	'''
	Function to render the step_8 page of "Behind the Calculations"

	Inputs:
		request: a request to step_8 of "Behind the Calculations"

	Returns:
		render: html template of the step_8 page
	'''
	return render(request, 'home/step_8.html')