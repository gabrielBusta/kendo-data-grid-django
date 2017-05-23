import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mwmtest.settings')
import django
django.setup()
from datagrid import models

employees = models.Employee.objects.all()

cities = {'HOU': 'Houston', 'LA': 'Los Angeles', 'CHI': 'Chicago',
'RED': 'Redmond', 'LON': 'London', 'PHI': 'Philadelphia', 'NY': 'New York',
'SEA': 'Seattle', 'AUS': 'Austin', 'BOS': 'Boston'}

for e in employees:
    e.city = cities[e.city]
    e.save()