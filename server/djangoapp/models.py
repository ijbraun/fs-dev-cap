

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'Suv'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('TRUCK', 'Truck'),
    ]
    validators = [MaxValueValidator(2023), MinValueValidator(2015)]
    type = models.CharField(max_length=10, choices=TYPES, default="SEDAN")
    year = models.IntegerField(default=2023,
                               validators=validators)

    def __str__(self):
        return self.name
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
