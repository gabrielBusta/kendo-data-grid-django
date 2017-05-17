import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mwmtest.settings')
import django
django.setup()
from datagrid import models
import random
import datetime

f = open('data.txt', encoding='UTF-8')
lines = f.readlines()
f.close()

rows = []
first = True
for line in lines:
    # skip the column names.
    if first:
        first = False
        continue
    first_name, last_name, city, job_title, birth_date = line.split('\t')
    rows.append({
        'first_name': first_name.rstrip(),
        'last_name': last_name.rstrip(),
        'job_title': job_title.rstrip(),
        'birth_date': birth_date.rstrip(),
    })

cities = ['HOU', 'LA', 'CHI', 'RED', 'LON', 'PHI', 'NY', 'SEA', 'AUS', 'BOS']
for row in rows:
    row['city'] = random.choice(cities)

for i in range(0, 50000):
    row = random.choice(rows)
    dob = datetime.datetime.strptime(row['birth_date'], "%m/%d/%Y").date()
    models.Employee.objects.create(
        first_name=row['first_name'],
        last_name=row['last_name'],
        job_title=row['job_title'],
        birth_date=dob,
        city=row['city'],
    )
