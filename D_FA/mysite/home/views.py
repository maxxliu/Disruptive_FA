from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'home/home.html')


def quick_search(request):
	return render(request, 'quick_search/quick_search.html')


def advanced_search(request):
	return render(request, 'advanced_search/advanced_search.html')


def info(request):
	return render(request, 'home/info.html')


def step_1(request):
	return render(request, 'home/step_1.html')


def step_2(request):
	return render(request, 'home/step_2.html')


def step_3(request):
	return render(request, 'home/step_3.html')


def step_4(request):
	return render(request, 'home/step_4.html')


def step_5(request):
	return render(request, 'home/step_5.html')


def step_6(request):
	return render(request, 'home/step_6.html')


def step_7(request):
	return render(request, 'home/step_7.html')


def step_8(request):
	return render(request, 'home/step_8.html')