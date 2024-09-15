from django.db import models
from category_management.models import *

class Product(models.Model):
	name = models.CharField(
		max_length=500,
		null=True,
		blank=True
	)
	category = models.ForeignKey(
		Category, 
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		related_name='product_category'
	)
	slug = models.SlugField(
		unique=True,
		max_length=500,
		null=True,
		blank=True
	)
	description = models.TextField(
		null=True,
		blank=True
	)
	item_code = models.CharField(
		max_length=20,
		null=True,
		blank=True
	)
	pack = models.IntegerField(
		default=1,
		null=True,
		blank=True
	)
	price = models.DecimalField(
		max_digits=10, 
		decimal_places=2,
		null=True,
		blank=True
	)
    inventory_count = models.IntegerField(
		default=0,
		null=True,
		blank=True
	)
    sales_count = models.IntegerField(
		default=0,
		null=True,
		blank=True
	)
	special_quantity = models.IntegerField(
		default=0,
		null=True,
		blank=True
	)
	special_price = models.DecimalField(
		max_digits=10, 
		decimal_places=2,
		null=True,
		blank=True
	)
	special_pack_bulk = models.CharField(
		max_length=2,
		default="P",
		null=True,
		blank=True
	)
	special_from = models.DateTimeField(
		null=True,
		blank=True
	)
	special_till = models.DateTimeField(
		null=True,
		blank=True
	)
	special_max = models.IntegerField(
		default=0,
		null=True,
		blank=True
	)
	onhand_stock = models.DecimalField(
		default=0,
		max_digits=10, 
		decimal_places=2,
		null=True,
		blank=True
	)
	size = models.CharField(
		max_length=20,
		null=True,
		blank=True
	)
	product_unit = models.CharField(
		max_length=50,
		null=True,
		blank=True
	)
	is_by_weight = models.BooleanField(
		default=False
	)
	tax = models.IntegerField(
		default=0,
		null=True,
		blank=True
	)
	discount = models.DecimalField(
		max_digits=10, 
		decimal_places=2,
		null=True,
		blank=True
	)
	image = models.TextField(
		null=True,
		blank=True
	)
	availableondays = models.CharField(
		max_length=255,
		null=True,
		blank=True
	)
	limitshopperbyday = models.DecimalField(
		max_digits=10, 
		decimal_places=2,
		null=True,
		blank=True
	)
	isdeleted = models.BooleanField(
		default=False
	)
	isactive = models.BooleanField(
		default=True
	)
	created_date = models.DateTimeField(
		auto_now_add=True
	)
	updated_date = models.DateTimeField(
		auto_now=True
	)
	created_by = models.IntegerField(
		null=True,
		blank=True
	)
	updated_by = models.IntegerField(
		null=True,
		blank=True
	)

	def __str__(self):
		return self.name
