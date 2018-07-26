from django.db import models

# Create your models here.

class WASHU(models.Model):
    name = models.CharField(max_length=30)
    contentid = models.CharField(max_length=30)
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class YSTEN(models.Model):
    name = models.CharField(max_length=30)
    contentid = models.CharField(max_length=30)
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

