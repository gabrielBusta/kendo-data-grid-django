from .models import Employee
from django.shortcuts import render
from django.http import JsonResponse
from itertools import islice


def index(request):
    '''Returns a template with a kendo-grid widget to display Employee data.'''
    return render(request, 'grid/index.html', {})


def employees(request):
    '''Returns Employee objects in the database as a list of Json objects.
GET request parameters:
    skip - how many data items to skip.
    take - the number of data items to return.'''
    
    # Fetch the paging parameters.
    skip = request.GET.get('skip', '')
    take = request.GET.get('take', '')
    
    employees = Employee.objects.all()

    # If a paging parameter is not recived:
    #     Create a list of dictionaries representing ALL Employee objects
    # else:
    #     Create a list of dictionaries representing the Employee objects in the desired range.
    if skip == '' or take == '':
        data = [employee.asdict() for employee in employees]
    else:
        skip = int(skip)
        take = int(take)
        data = [employee.asdict() for employee in islice(employees, skip, skip + take)]

    # { "data": [ /* employee Json objects */ ], ... }
    return JsonResponse({'data': data, 'total': len(employees)})
    

def titles(request):
    '''Returns a Json list of all possible values for an Employee's job_title.'''
    data = list(Employee.objects.values_list('job_title', flat=True).distinct())
    return JsonResponse({'data': data, 'total': len(data)})
    
    
def cities(request):
    '''Returns a Json list of all the possible choices for an Employee's city.'''
    data = [choice[1] for choice in Employee.CITY_CHOICES]
    return JsonResponse({'data': data, 'total': len(data)})