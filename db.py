import random
first = True
f = open('data.txt', encoding='UTF-8')
rows = []
for line in f.readlines():
    if first:
        first = False
        continue
    first_name, last_name, city, job_title, birth_date = line.split('\t')
    rows.append({
        'first_name': first_name,
        'last_name': last_name,
        'job_title': job_title,
        'birth_date': birth_date,
    })
cities = ['Houston', 'Los Angeles', 'Chicago', 'Redmond', 'London', 'Philadelphia', 'New York', 'Seattle', 'Austin', 'Boston']
for row in rows:
    row['city'] = random.choice(cities)
for i in range(0, 10):
    print(random.choice(rows))
