from django.shortcuts import render
from django.db.models import Count, Sum
from rest_framework import mixins, viewsets, response, request, status, views, permissions
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .serializers import (IncomeSerializer,
                          CategorySerializer,
                          WasteSerializer)
from .models import (Income, 
                     Waste, 
                     Category)

# Create your views here.
class IncomeViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet,):
  serializer_class = IncomeSerializer
  queryset = Income.objects.all().order_by('created').reverse()
  lookup_field = 'slug'
  

class NestedCategoryViewSet(viewsets.GenericViewSet):
  serializer_class = CategorySerializer
  queryset = Category.objects.all()
  lookup_field = 'slug'
  
  def retrieve(self, request: request.Request, slug: str, income_slug: str):
    try:
      income = Income.objects.get(slug = income_slug)
    except:
      return response.Response({'detail': 'not such income'}, status=status.HTTP_404_NOT_FOUND)
    
    instance = self.get_object()
    serializer = CategorySerializer(instance)
    data = serializer.data
    data.update(self.get_statistic(slug, income.slug))
    return response.Response(data)
  
  def list(self, request: request.Request, income_slug: str):
    try:
      income = Income.objects.get(slug = income_slug)
    except:
      return response.Response({'detail': 'not such income'}, status=status.HTTP_404_NOT_FOUND)
    
    queryset = self.get_queryset()
    serializer = CategorySerializer(queryset, many=True)
    data = serializer.data
    
    for i in data:
      i.update(self.get_statistic(i['slug'], income.slug))
  
    return response.Response(data)
  
  def get_statistic(self, slug: str, income_slug: str):
    wastes_sum = 0
    wastes_queryset = Waste.objects.filter(income__slug = income_slug, cat__slug = slug)

    if wastes_queryset:
      wastes_sum = wastes_queryset.aggregate(sum = Sum('amount'))['sum']
  
    return {
      'total': wastes_sum,
    }

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
  serializer_class = CategorySerializer
  queryset = Category.objects.all()
  lookup_field = 'slug'


class NestedWasteViewSet(
                         viewsets.GenericViewSet):
  queryset = Waste.objects.all()
  serializer_class = WasteSerializer
  
  def retrieve(self, request: request.Request, income_slug, cat_slug, pk):
    try:
      instance = Waste.objects.get(pk = pk, income__slug = income_slug, cat__slug = cat_slug)
    except:
      return response.Response({'error': 'Waste not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WasteSerializer(instance)
    return response.Response(serializer.data)
  
  def list(self, request: request.Request, income_slug, cat_slug):
    queryset = Waste.objects.filter(income__slug = income_slug, cat__slug = cat_slug).order_by('created').reverse()
    if not queryset:
      return response.Response({'error': 'list is empty'}, status=status.HTTP_404_NOT_FOUND)
    serializer = WasteSerializer(queryset, many=True)
    return response.Response(serializer.data)
  
  def post(self, request: request.Request, income_slug, cat_slug):
    income = None
    cat = None
    
    try:
      income = Income.objects.get(slug = income_slug)
    except:
      return response.Response({'error': 'Income not exists'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
      cat = Category.objects.get(slug = cat_slug)
    except:
      return response.Response({'error': 'Category not exists'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WasteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(income = income, cat = cat, creator = request.user)
    
    return response.Response({'good'})

class WasteViewSet(mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
  queryset = Waste.objects.all()
  serializer_class = WasteSerializer

class VerifyToken(views.APIView):
  permission_classes = [permissions.IsAuthenticated]
  def get(self, request: request.Request):
    return response.Response(['token valid'])