from django.db import models
from passlib.hash import pbkdf2_sha256 as pbkdf

# Create your models here.
class Admin(models.Model):
    username=models.CharField(max_length=32)
    password_hash=models.CharField(max_length=128)

    def set_password(self, password):
        self.password_hash=pbkdf.hash(password)
        return

    def check_password(self, password):
        return pbkdf.verify(password, self.password_hash)

class Employee(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    ed=models.CharField(max_length=32)
    role=models.CharField(max_length=32)
