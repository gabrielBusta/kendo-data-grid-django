import json
from .models import Employee
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'grid/index.html', {})


def employees(request):
    data = map(lambda employee: {
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'city': employee.get_city_display(),
        'job_title': employee.job_title,
        'birth_date': str(employee.birth_date),
    }, Employee.objects.all())
    
    data = list(data)
    
    data = json.dumps(data)
    
    return HttpResponse(data, content_type='application/json')
    
    
def titles(request):
    data = list(Employee.objects.values_list('job_title', flat=True).distinct())
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
    
    
def cities(request):
    data = []
    for choice in Employee.CITY_CHOICES:
        data.append(choice[1])
    
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')