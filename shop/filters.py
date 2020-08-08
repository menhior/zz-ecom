import django_filters
from django_filters import DateFilter, CharFilter
from django import forms

from .models import *

class ProductFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control',
	 'type':"text", 'placeholder':"Search for products, brands and more...", 'size':"80"}))

	class Meta:
		model = Product
		fields = ['name']

class CustomerPageOrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_ordered", lookup_expr='gte', label = 'Start Date (mm/dd/yy)')
	end_date = DateFilter(field_name="date_ordered", lookup_expr='lte', label = 'End Date (mm/dd/yy)')
	status = CharFilter(field_name='status', lookup_expr='icontains')
	transaction_id = CharFilter(field_name='transaction_id', lookup_expr='icontains')


	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_ordered', 'complete']

class OrderListFilter(django_filters.FilterSet):
	
	transaction_id = CharFilter(field_name='transaction_id', lookup_expr='icontains')
	start_date = DateFilter(field_name="date_ordered", lookup_expr='gte', label = 'Start Date (mm/dd/yy)')
	end_date = DateFilter(field_name="date_ordered", lookup_expr='lte', label = 'End Date (mm/dd/yy)')
	



	class Meta:
		model = Order
		fields = '__all__'
		exclude = [ 'date_ordered', 'complete']


class CustomerListFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr='icontains')
	phone = CharFilter(field_name='phone', lookup_expr='icontains')
	email = CharFilter(field_name='email', lookup_expr='icontains')
	device = CharFilter(field_name='device', lookup_expr='icontains')
	start_date = DateFilter(field_name="date_created", lookup_expr='gte', label = 'Start Date (mm/dd/yy)')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte', label = 'End Date (mm/dd/yy)')
	



	class Meta:
		model = Customer
		fields = '__all__'
		exclude = [ 'user', 'date_created', 'profile_pic']