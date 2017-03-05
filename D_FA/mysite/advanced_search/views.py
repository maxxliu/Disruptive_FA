from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'advanced_search/advanced_search.html')

def results(request):
	return None