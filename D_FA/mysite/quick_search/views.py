from django.shortcuts import render, HttpResponse
from .models import Stock
from django.core.exceptions import *

# Create your views here.
def index(request):
	return render(request, 'quick_search/quick_search.html')

def results(request):
	return None
# 	if request.method == 'POST':
#         search_id = request.POST.get('textfield', None)
#         try:
#             search = Stock.objects.get(name = search_id)
#             #do something with search
#             html = ("<H1>%s</H1>", search)
#             return HttpResponse(html)
#         except Stock.DoesNotExist:
#             return HttpResponse("no such stock")  
#     else:
#         return render(request, 'quick_search/quick_search.html')