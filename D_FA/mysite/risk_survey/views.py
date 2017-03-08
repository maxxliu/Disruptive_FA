from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
	return render(request, 'risk_survey/risk_survey.html')

def scored(request):
	return HttpResponse("<p>Thanks!</p>")