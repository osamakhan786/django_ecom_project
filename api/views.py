from distutils.log import info
from unicodedata import name
from django.http import JsonResponse

# Create your views here.
def home(request):
    return JsonResponse({'info': 'django react cource', 'name':'osama'})