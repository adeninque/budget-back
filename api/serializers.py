from rest_framework import serializers
from django.db.models import Sum
from django.utils.text import slugify
from datetime import datetime

import shortuuid

from .models import *

class SlugMixin:
  def add_slug(self, validated_data, model):
    validated_data['slug'] = slugify(validated_data['title'])
    
    if model.objects.filter(slug = validated_data['slug']).exists():
      validated_data['slug'] = f'{validated_data["slug"]}-{shortuuid.uuid()[:8]}'
    
    return validated_data


class IncomeSerializer(SlugMixin, serializers.ModelSerializer):
  class Meta:
    model = Income
    fields = '__all__'
    read_only_fields = ('created', 'id', 'slug')
  
  def to_representation(self, instance: Income):
    data = super().to_representation(instance)
    wastes = 0
    waste_set = instance.waste_set.all()
    
    if len(waste_set) > 0:
      wastes = waste_set.aggregate(sum = Sum('amount'))['sum'] 
    
    data.update({
      'wastes': wastes,
      'remains': data['budget'] - wastes
    })

    data['created'] = datetime.strftime(instance.created, '%Y-%m-%d at %H:%M')
    
    return data
  
  def create(self, validated_data):
    validated_data = self.add_slug(validated_data, self.Meta.model)
    return super().create(validated_data)
  

class CategorySerializer(SlugMixin, serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'
    read_only_fields = ('slug', 'created', 'id')
    
  def create(self, validated_data):
    validated_data = self.add_slug(validated_data, self.Meta.model)
    
    return super().create(validated_data)
  
  def update(self, instance, validated_data):
    validated_data = self.add_slug(validated_data, self.Meta.model)
    
    return super().update(instance, validated_data)

class WasteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Waste
    fields = '__all__'
    read_only_fields = ('created', 'id', 'income', 'cat')