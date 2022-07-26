import django_filters
from django import forms
from django_filters import CharFilter, filters

from .models import *


# class ProductFilter(django_filters.FilterSet):
#     title = CharFilter(field_name='title', label='', lookup_expr='icontains', widget=forms.TextInput(attrs={
#         'placeholder': 'Search Title ', 'class': 'form-control'}))
#     category = filters.ModelChoiceFilter(label="", queryset=DressCategory.objects.all())
#
#     class Meta:
#         model = product
#         fields = ('title', 'category')


class UserFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', label="", lookup_expr='icontains', )

    class Meta:
        model = Customer
        fields = ('name',)




class OrderFilter(django_filters.FilterSet):
    id = CharFilter(field_name='id', label='Order ID', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'placeholder': 'Search Order ID ', 'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ('id',)


