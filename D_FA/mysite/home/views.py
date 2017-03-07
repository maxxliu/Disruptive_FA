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