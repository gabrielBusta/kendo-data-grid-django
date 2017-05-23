from .models import Employee
from django.shortcuts import render
from django.http import JsonResponse
from querystring_parser import parser
from itertools import islice


def index(request):
    '''Returns a template with a kendo-grid widget to display Employee data.'''
    return render(request, 'grid/index.html', {})


def employees(request):
    '''Returns Employee objects in the database as a list of Json objects.
GET request parameters:
    skip - how many data items to skip.
    take - the number of data items to return.'''
    
    # Fetch the request parameters.
    args = getargs(request)
    employees = Employee.objects.all()
    
    if args['filters'] is not None:
        for i in args['filters']:
            kwargs = {args['filters'][i]['field']: args['filters'][i]['value']}
            if args['filters'][i]['operator'] == 'eq':
                employees = employees.filter(**kwargs)
                print(len(employees))
            if args['filters'][i]['operator'] == 'neq':
                employees = employees.exclude(**kwargs)

    # If a paging parameter is not recived:
    #     Create a list of dictionaries representing ALL Employee objects
    # else:
    #     Create a list of dictionaries representing the Employee objects in the desired range.
    if args['skip'] == None or args['take'] == None:
        data = [employee.asdict() for employee in employees]
    else:
        data = [employee.asdict() for employee in islice(employees, args['skip'], args['skip'] + args['take'])]

    # { "data": [ /* employee Json objects */ ], ... }
    return JsonResponse({'data': data, 'total': len(employees)})
    

def getargs(request):
    '''Returns the arguments sent in the request as a dictionary.'''
    args = parser.parse(request.GET.urlencode())
    
    skip = args.get('skip', None)
    if skip is not None:
        skip = int(skip)
    
    take = args.get('take', None)
    if take is not None:
        take = int(take)
    
    filters = args.get('filter', None)
    if filters is not None:
        filters = filters.get('filters', None)
    
    return {'skip': skip, 'take': take, 'filters': filters}


def titles(request):
    '''Returns a Json list of all possible values for an Employee's job_title.'''
    data = list(Employee.objects.values_list('job_title', flat=True).distinct())
    return JsonResponse({'data': data, 'total': len(data)})
    
    
def cities(request):
    '''Returns a Json list of all the possible choices for an Employee's city.'''
    data = [choice[1] for choice in Employee.CITY_CHOICES]
    return JsonResponse({'data': data, 'total': len(data)})