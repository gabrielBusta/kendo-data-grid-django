import json
from datetime import date
from django.test import TestCase, Client
from datagrid.models import Employee
import datagrid.views as views


class EmployeeTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(
            first_name='Marissa',
            last_name='Genders',
            job_title='Account Coordinator',
            birth_date=date(1992, 5, 26),
            city=Employee.CHICAGO,
        )
        Employee.objects.create(
            first_name='Miguel',
            last_name='Sanchez',
            job_title='Technical Writer',
            birth_date=date(1989, 3, 28),
            city=Employee.AUSTIN,
        )
        Employee.objects.create(
            first_name='Carlyn',
            last_name='Uridge',
            job_title='Web Developer',
            birth_date=date(1962, 6, 15),
            city=Employee.PHILADELPHIA,
        )

    def test_employee_model(self):
        '''Test the Employee model by fetching objects and checking their attributes.'''
        marissa = Employee.objects.get(first_name='Marissa')
        miguel = Employee.objects.get(first_name='Miguel')
        carlyn = Employee.objects.get(first_name='Carlyn')
        
        self.assertEqual(marissa.last_name, 'Genders')
        self.assertEqual(marissa.job_title, 'Account Coordinator')
        self.assertEqual(marissa.birth_date, date(1992, 5, 26))
        self.assertEqual(marissa.city, Employee.CHICAGO)
        
        self.assertEqual(miguel.last_name, 'Sanchez')
        self.assertEqual(miguel.job_title, 'Technical Writer')
        self.assertEqual(miguel.birth_date, date(1989, 3, 28))
        self.assertEqual(miguel.city, Employee.AUSTIN)
        
        self.assertEqual(carlyn.last_name, 'Uridge')
        self.assertEqual(carlyn.job_title, 'Web Developer')
        self.assertEqual(carlyn.birth_date, date(1962, 6, 15))
        self.assertEqual(carlyn.city, Employee.PHILADELPHIA)


class TitlesViewTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(
            first_name='Marissa',
            last_name='Genders',
            job_title='Account Coordinator',
            birth_date=date(1992, 5, 26),
            city=Employee.CHICAGO,
        )
        Employee.objects.create(
            first_name='Miguel',
            last_name='Sanchez',
            job_title='Technical Writer',
            birth_date=date(1989, 3, 28),
            city=Employee.AUSTIN,
        )
        Employee.objects.create(
            first_name='Carlyn',
            last_name='Uridge',
            job_title='Web Developer',
            birth_date=date(1962, 6, 15),
            city=Employee.PHILADELPHIA,
        )

    def test_titles_view(self):
        '''Test the /titles/ JSON API endpoint by asserting the possible values of an employee's job title.'''
        job_titles = ['Account Coordinator', 'Technical Writer', 'Web Developer']
        client = Client()
        response = client.get('/titles/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.getvalue().decode())
        self.assertCountEqual(data, job_titles)


class CitiesViewTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(
            first_name='Marissa',
            last_name='Genders',
            job_title='Account Coordinator',
            birth_date=date(1992, 5, 26),
            city=Employee.CHICAGO,
        )
        Employee.objects.create(
            first_name='Miguel',
            last_name='Sanchez',
            job_title='Technical Writer',
            birth_date=date(1989, 3, 28),
            city=Employee.AUSTIN,
        )
        Employee.objects.create(
            first_name='Carlyn',
            last_name='Uridge',
            job_title='Web Developer',
            birth_date=date(1962, 6, 15),
            city=Employee.PHILADELPHIA,
        )

    def test_cities_view(self):
        '''Test the /cities/ JSON API endpoint by asserting the possible values of an employee's city attribute.'''
        cities = [choice[1] for choice in Employee.CITY_CHOICES]
        client = Client()
        response = client.get('/cities/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.getvalue().decode())
        self.assertCountEqual(data, cities)
        
        
class EmployeesViewTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(
            first_name='Marissa',
            last_name='Genders',
            job_title='Account Coordinator',
            birth_date=date(1992, 5, 26),
            city=Employee.CHICAGO,
        )
        Employee.objects.create(
            first_name='Miguel',
            last_name='Sanchez',
            job_title='Technical Writer',
            birth_date=date(1989, 3, 28),
            city=Employee.AUSTIN,
        )
        Employee.objects.create(
            first_name='Carlyn',
            last_name='Uridge',
            job_title='Web Developer',
            birth_date=date(1962, 6, 15),
            city=Employee.PHILADELPHIA,
        )

    def test_employees_view(self):
        '''Test the /employees/ JSON API endpoint by asserting the attributes of the employees and their content.'''
        client = Client()
        response = client.get('/employees/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.getvalue().decode())
        self.assertCountEqual(
            data[0].keys(),
            ['FirstName', 'LastName', 'Title', 'BirthDate', 'City'],
        )
        for employee in data:
            if employee['FirstName'] == 'Marissa':
                self.assertEqual(employee['LastName'], 'Genders')
                self.assertEqual(employee['Title'], 'Account Coordinator')
                self.assertEqual(employee['BirthDate'], '1992-05-26')
                self.assertEqual(employee['City'], 'Chicago')
            if employee['FirstName'] == 'Miguel':
                self.assertEqual(employee['LastName'], 'Sanchez')
                self.assertEqual(employee['Title'], 'Technical Writer')
                self.assertEqual(employee['BirthDate'], '1989-03-28')
                self.assertEqual(employee['City'], 'Austin')
            if employee['FirstName'] == 'Carlyn':
                self.assertEqual(employee['LastName'], 'Uridge')
                self.assertEqual(employee['Title'], 'Web Developer')
                self.assertEqual(employee['BirthDate'], '1962-06-15')
                self.assertEqual(employee['City'], 'Philadelphia')

 
class IndexViewTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(
            first_name='Marissa',
            last_name='Genders',
            job_title='Account Coordinator',
            birth_date=date(1992, 5, 26),
            city=Employee.CHICAGO,
        )
        Employee.objects.create(
            first_name='Miguel',
            last_name='Sanchez',
            job_title='Technical Writer',
            birth_date=date(1989, 3, 28),
            city=Employee.AUSTIN,
        )
        Employee.objects.create(
            first_name='Carlyn',
            last_name='Uridge',
            job_title='Web Developer',
            birth_date=date(1962, 6, 15),
            city=Employee.PHILADELPHIA,
        )

    def test_index_view(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)