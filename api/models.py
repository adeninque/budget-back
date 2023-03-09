from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
  title = models.CharField(max_length = 255)
  budget = models.IntegerField()
  created = models.DateTimeField(auto_now_add = True)
  slug = models.SlugField(unique=True, null=False)
  
  def __str__(self):
    return self.title

class Category(models.Model):
  title = models.CharField(max_length = 255)
  slug = models.SlugField(unique=True, null=False)
  
  def __str__(self):
    return self.title

class Waste(models.Model):
  purpose = models.CharField(max_length = 255)
  amount = models.IntegerField()
  created = models.DateTimeField(auto_now_add = True)
  cat = models.ForeignKey('Category', on_delete = models.PROTECT)
  creator = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
  income = models.ForeignKey('Income', on_delete = models.CASCADE)
  
  def __str__(self):
    return self.purpose