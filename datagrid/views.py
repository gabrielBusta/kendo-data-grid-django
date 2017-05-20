from .models import Employee
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    '''Returns a template displaying a full screen kendo-grid widget.'''
    return render(request, 'grid/index.html', {})


def employees(request):
    '''Returns every Employee in the database as a list of Json objects.'''
    # Create a list of dictionaries representing Employee objects.
    data = list(map(lambda employee: {
        'FirstName': employee.first_name,
        'LastName': employee.last_name,
        'City': employee.get_city_display(),
        'Title': employee.job_title,
        'BirthDate': str(employee.birth_date),
    }, Employee.objects.all()))
    # { "data": [ /* employee objects */ ], ... }
    return JsonResponse({'data': data, 'total': len(data)})
    

def titles(request):
    '''Returns a Json list of all possible values for an Employee's job_title.'''
    data = list(Employee.objects.values_list('job_title', flat=True).distinct())
    return JsonResponse({'data': data, 'total': len(data)})
    
    
def cities(request):
    '''Returns a Json list of all the possible choices for an Employee's city.'''
    data = [choice[1] for choice in Employee.CITY_CHOICES]
    return JsonResponse({'data': data, 'total': len(data)})