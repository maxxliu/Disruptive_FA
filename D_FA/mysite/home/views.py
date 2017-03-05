from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'home/home.html')

def quick_search(request):
	return render(request, 'quick_search/quick_search.html')