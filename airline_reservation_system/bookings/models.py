import random

from django.db import models


class Flight(models.Model):
    def generate_pk():
        number = random.randint(1000, 9999)
        return 'flight-{}'.format(number)

    id = models.CharField(default=generate_pk, primary_key=True, max_length=255, unique=True)
    flight_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    no_of_seats = models.PositiveBigIntegerField()
    remaining_seats = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.flight_name

class Booking(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)

    def generate_pk():
        number = random.randint(1000, 9999)
        return 'book-{}'.format(number)

    id = models.CharField(default=generate_pk, primary_key=True, max_length=255, unique=True)    
    email = models.EmailField()
    name = models.CharField(max_length=30)
    user_id =models.DecimalField(decimal_places=0, max_digits=2)
    flight_id=models.CharField(max_length=30)
    flight_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    no_of_seats = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=100)

    def __str__(self):
        return self.email

