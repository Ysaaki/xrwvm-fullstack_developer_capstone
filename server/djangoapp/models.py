# Uncomment the following imports before adding the Model code

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    class CarType(models.TextChoices):
        SUV = "SUV", "SUV"
        SEDAN = "Sedan", "Sedan"
        COUPE = "Coupe", "Coupe"
        MINIVAN = "Minivan", "Minivan"
        CONVERTIBLE = "Convertible", "Convertible"
        PICKUP = "Pickup", "Pickup"
        HATCHBACK = "Hatchback", "Hatchback"

    # Many-To-One relationship to Car Make model
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # CharField choices require a max_length set
    type = models.CharField(
        max_length=20, choices=CarType.choices, default=CarType.SUV
    )

    # Removed max_length parameter since it is invalid for IntegerField
    year = models.IntegerField(
        validators=[MaxValueValidator(2023), MinValueValidator(2015)]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
