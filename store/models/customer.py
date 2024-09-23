from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=255, default='')  # Tambahkan default di sini
    email = models.EmailField(max_length=100)
    bank = models.CharField(max_length=50, default='')

    def register(self):
        self.save()

    def isExists(self):
        return Customer.objects.filter(username=self.username).exists()