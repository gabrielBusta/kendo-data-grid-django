from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    birth_date = models.DateField()

    # define city choices and then a city field.

    HOUSTON = 'HOU'
    LOS_ANGELES = 'LA'
    CHICAGO = 'CHI'
    REDMOND = 'RED'
    LONDON = 'LON'
    PHILADELPHIA = 'PHI'
    NEW_YORK = 'NY'
    SEATTLE = 'SEA'
    AUSTIN = 'AUS'
    BOSTON = 'BOS'

    CITY_CHOICES = (
        (HOUSTON, 'Houston'),
        (LOS_ANGELES, 'Los Angeles'),
        (CHICAGO, 'Chicago'),
        (REDMOND, 'Redmond'),
        (LONDON, 'London'),
        (PHILADELPHIA, 'Philadelphia'),
        (NEW_YORK, 'New York'),
        (SEATTLE, 'Seattle'),
        (AUSTIN, 'Austin'),
        (BOSTON, 'Boston'),
    )

    city = models.CharField(
        max_length=3,
        choices=CITY_CHOICES,
        default=HOUSTON,
    )