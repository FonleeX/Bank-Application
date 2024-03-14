from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True,)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    city = models.CharField(max_length = 64, defualt="Lincoln")
    address = models.TextField(max_length=200, defualt="Brayford Pool")
    postcode = models.CharField(max_length=8, )
    #postcode
    

    email = models.EmailField(unique=True, max_length = 254)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
