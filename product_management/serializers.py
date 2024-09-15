from rest_framework import serializers
from django.contrib.auth.models import User
# from customer.models import *
from django.utils.text import slugify

class ProductSerializer(serializers.Serializer):
	description=serializers.CharField(
		required=True,
		max_length=255
	)
	item_code=serializers.CharField(
		required=True,
		max_length=20,
	)
	pack=serializers.IntegerField(
		required=False,
		allow_null=True,
		default=1
	)
	price=serializers.DecimalField(
		required=True,
		max_digits=10,
		decimal_places=2,
		coerce_to_string=False
	)
	special_quantity=serializers.IntegerField(
		required=False,
		allow_null=True,
		default=0
	)
	special_price=serializers.DecimalField(
		required=False,
		max_digits=10,
		decimal_places=2,
		default=0,
		coerce_to_string=False
	)
	special_pack_bulk=serializers.ChoiceField(
		required=False,
		default="P",
		choices=(
			("P", "Pack"),
			("M", "Minimum"),
			("B", "Bulk"),
		),
		help_text="pass P, M or B"
	)
	special_from=serializers.DateField(
		required=False,
		format="%Y-%m-%d",
		allow_null=True,
		help_text="date format YYYY-MM-DD like 2022-07-13"
	)
	special_till=serializers.DateField(
		required=False,
		format="%Y-%m-%d",
		allow_null=True,
		help_text="date format YYYY-MM-DD like 2023-04-25"
	)
	special_max=serializers.IntegerField(
		required=False,
		allow_null=True,
		default=0
	)
	onhand_stock=serializers.IntegerField(
		required=False,
		allow_null=True,
		default=0
	)
	size=serializers.CharField(
		required=False,
		max_length=20,
		allow_null=True,
		allow_blank=True
	)
	product_unit=serializers.CharField(
		required=False,
		max_length=15,
		allow_null=True,
		allow_blank=True
	)
	is_by_weight=serializers.BooleanField(
		required=False,
		default=False
	)
	tax=serializers.DecimalField(
		required=False,
		max_digits=10,
		decimal_places=3,
		default=0,
		coerce_to_string=False
	)
	discount=serializers.DecimalField(
		required=False,
		max_digits=10,
		decimal_places=3,
		default=0,
		coerce_to_string=False
	)
	image=serializers.CharField(
		required=False,
		allow_null=True,
		allow_blank=True
	)
	availableondays=serializers.CharField(
		required=False,
		allow_null=True,
		allow_blank=True
	)
	limitshopperbyday=serializers.CharField(
		required=False,
		allow_null=True,
		allow_blank=True
	)
	isactive=serializers.BooleanField(
		required=False,
		default=True
	)
	@classmethod
	def validate(self, data):
		errors = {}

		if errors:
			raise serializers.ValidationError(errors)

		return super(ProductSerializer, self).validate(self, data)

class ProductUpdateSerializer(ProductSerializer):
	product_id = serializers.IntegerField(
		required=True
	)
	@classmethod
	def validate(self, data):
		errors = {}
		if errors:
			raise serializers.ValidationError(errors)

		return super(ProductUpdateSerializer, self).validate(data)

class ProductByIDSerializer(serializers.Serializer):
	barcode = serializers.CharField(
		required=True
	)
	@classmethod
	def validate(self, data):
		errors = {}
		barcode = data.get("barcode")
		barcode = barcode.strip()
		store_id = data.get("store_id")
		if not Product.objects.filter(
			item_code=barcode,
			store_id=store_id,
			isactive=True,
			isdeleted=False
		).exists():
			errors["barcode"]= "No active product found in your store"
		if errors:
			raise serializers.ValidationError(errors)

		return super(ProductByIDSerializer, self).validate(self, data)
class ProductChangeSerializer(serializers.Serializer):
	product_ids = serializers.CharField(
		required=True
	)
	@classmethod
	def validate(self, data):
		errors = {}
		if errors:
			raise serializers.ValidationError(errors)
		return super(ProductChangeSerializer, self).validate(self, data)


class PopularProductSerializer(serializers.Serializer):
	status = serializers.BooleanField(
		required=True
	)
	product_ids = serializers.CharField(
		required=True
	)
	@classmethod
	def validate(self, data):

		errors = {}
		if errors:
			raise serializers.ValidationError(errors)
		return super(PopularProductSerializer, self).validate(self, data)


class SaleCountUpdateSerializer(serializers.Serializer):
    product_id = serializers.CharField(
		required=True
	)
	product_count = serializers.IntegerField(
		required=True,
		min_value=0
	)
	@classmethod
	def validate(self, data):

		errors = {}
		if errors:
			raise serializers.ValidationError(errors)
		return super(SaleCountUpdateSerializer, self).validate(self, data)

class ProductStatusChangeSerializer(serializers.Serializer):
	product_ids = serializers.CharField(
		required=True
	)
	status = serializers.BooleanField(
		required=True
	)
	@classmethod
	def validate(self, data):
		errors = {}
		if errors:
			raise serializers.ValidationError(errors)
		return super(ProductStatusChangeSerializer, self).validate(self, data)

class KeyErrorSerializer(serializers.Serializer):
	error = serializers.CharField(
		required=False,
		help_text="Key error. Please check the error message"
	)

	@classmethod
	def validate(self, data):
		errors = {}

		if errors:
			raise serializers.ValidationError(errors)

		return super(KeyErrorSerializer, self).validate(self, data)

class ProductListSerializer(serializers.Serializer):
	search = serializers.CharField(
		required=False,
		allow_null=True,
		allow_blank=True,
		max_length=250,
		help_text="Pass search keyword here. Leave blank if do not want to search."
	)
	limit = serializers.IntegerField(
		required=False,
		min_value=1,
		default=10,
		help_text="Pass limit in integer. Default is 10."
	)
	page = serializers.IntegerField(
		required=False,
		min_value=1,
		default=1
	)
	order = serializers.CharField(
		required=False,
		max_length=250,
		default="id",
		help_text="Pass field name for ordering. Use '-' before field name to order descending. Default order is ID."
	)
	status = serializers.ChoiceField(
		required=False,
		default="all",
		choices=(
			("true", "true"),
			("false", "false"),
			("all", "all"),
		),
		help_text="Options are true, false, all."
	)

	@classmethod
	def validate(self, data):
		errors = {}

		if errors:
			raise serializers.ValidationError(errors)

		return super(ProductListSerializer, self).validate(self, data)

