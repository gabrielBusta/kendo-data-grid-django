from .models import Employee
from django.shortcuts import render
from django.http import JsonResponse
from querystring_parser import parser as argparser
from dateutil import parser as dateparser
from itertools import islice
import datetime


def index(request):
    '''Returns a template with a kendo-grid widget to display Employee data.'''
    return render(request, 'grid/index.html', {})


def employees(request):
    '''Returns Employee objects in the database as a list of Json objects.
GET request parameters:
    skip - how many data items to skip.
    take - the number of data items to return (i.e. the pageSize).
    filters - filtering criteria for employees objects. 
    '''
    
    # Parse the request arguments.
    args = getargs(request)
    
    employees = Employee.objects.all()
    
    if args['filters'] != '':
        employees = applyfilters(employees, args['filters'])

    if args['sort'] != '':
        employees = applysort(employees, args['sort'])

    if args['skip'] == '' or args['take'] == '':
        data = [employee.asdict() for employee in employees]
    else:
        data = [employee.asdict() for employee in getslice(employees, args['skip'], args['take'])]

    # { "data": [ /* employee Json objects */ ], ... }
    return JsonResponse({'data': data, 'total': len(employees)})
    

def getargs(request):
    '''Returns the arguments sent in the request as a dictionary in this format:
args = {
    'skip': the number of employees to skip or '' if the argument was not recieved.
    'take': the number of employees to return or '' if the argument was not recieved.
    'filters': {
        index: {
            'field': the name of the field to use for filtering.
            'value': the value used to filter the field.
            'operator': a string representing the logical operator used to filter
                        the field. e.g. eq for equals to, lt for less than, ect.
    }
}
'''
    args = argparser.parse(request.GET.urlencode())

    skip = args.get('skip', '')
    if skip != '':
        skip = int(skip)
    
    take = args.get('take', '')
    if take != '':
        take = int(take)
        
    sort = args.get('sort', '')
    if sort != '':
        sort = sort[0]
    
    filters = args.get('filter', '')
    if filters != '':
        filters = filters.get('filters', '')
    
    return {'skip': skip, 'take': take, 'filters': filters, 'sort': sort}


def applyfilters(employees, filters):
    '''Applies the desired filters to an Employee query set.
Returns the filtered query set. filters must be a dictionary in this format:
filters = {
    index: {
            'field': the name of the field to use for filtering.
            'value': the value used to filter the field.
            'operator': a string representing the logical operator used to filter
                        the field. e.g. eq for equals to, lt for less than, ect.
    }
}'''
    for index in filters:
        # If we are filtering using the city field we need to
        # convert the display name of the city into it's real value.
        if filters[index]['field'] == 'city':
            for value, display in Employee.CITY_CHOICES:
                if display == filters[index]['value']:
                    filters[index]['value'] = value

        # If we are filtering using the birth_date field we need to
        # convert the date string into a date object.
        if filters[index]['field'] == 'birth_date':
            filters[index]['value'] = dateparser.parse(
                filters[index]['value'],
                fuzzy=True,
            ).date() # cast the datetime object into a date object.
        
        if filters[index]['operator'] == 'eq' or filters[index]['operator'] == 'neq':
            kwargs = {filters[index]['field']: filters[index]['value']}
            if filters[index]['operator'] == 'eq':
                employees = employees.filter(**kwargs)
            elif filters[index]['operator'] == 'neq':
                employees = employees.exclude(**kwargs)
        else:
            kwargs = {'{}__{}'.format(filters[index]['field'], filters[index]['operator']): filters[index]['value']}
            employees = employees.filter(**kwargs)
                
    return employees


def applysort(employees, sort):
    '''Applies the desired sort to an Employee query set.
Returns the sorted query set. the sort must be a dictionary in this format:
sort = {
    'dir': the direction of the sort (asc or desc),
    'field': the name of the field to sort by.
}'''
    if sort['dir'] == 'desc':
        sort['field'] = '-{}'.format(sort['field'])
    return employees.order_by(sort['field'])


def getslice(iterable, skip, take):
    '''Skips 'skip' items then grabs 'take' items from a iterable sequence.
Returns a generator containing the desired slice of the iterable sequence.
If we run out of items to take, after skiping 'skip' items, we just take items util we exhaust the squence.'''
    if skip + take > len(iterable):
        return islice(iterable, skip, None)
    else:
        return islice(iterable, skip, skip + take)


def titles(request):
    '''Returns a Json list of all possible values for an Employee's job_title.'''
    data = list(Employee.objects.values_list('job_title', flat=True).distinct())
    return JsonResponse({'data': data, 'total': len(data)})
    
    
def cities(request):
    '''Returns a Json list of all the possible choices for an Employee's city.'''
    data = [choice[1] for choice in Employee.CITY_CHOICES]
    return JsonResponse({'data': data, 'total': len(data)})