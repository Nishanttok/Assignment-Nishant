from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from product_management.serializers import *
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser
import json
from decimal import Decimal
from datetime import datetime

class ProductView(GenericAPIView):
	"""
		product add edit api
	"""
	parser_classes = (MultiPartParser,)
	permission_classes = [IsAuthenticated]
	serializer_class = ProductSerializer

	@classmethod
	@swagger_auto_schema(operation_summary=" Product add api",tags=['Product'])
	def post(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.data
		data = data.copy()
		if "product_id" in data:
			data.pop("product_id")
		data.update({
			"user_id":request.user.id
		})
		data_validation = ProductSerializer(data=data)
		is_valid_data = data_validation.is_valid()

		if is_valid_data:
			data = data_validation.validated_data
			ProductCreateOrUpdate.CreateOrUpdate(self,data)
			response['result'] = "product successfully added"	
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)

	@classmethod
	@swagger_auto_schema(operation_summary=" Product update api", request_body=ProductUpdateSerializer, tags=['Product'])
	def put(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.data
		data = data.copy()
		if "product_id" not in data:
			data["product_id"] = 0
		data.update({
			"user_id":request.user.id
		})
		data_validation = ProductUpdateSerializer(data=data)
		is_valid_data = data_validation.is_valid()

		if is_valid_data:
			data = data_validation.validated_data
			ProductCreateOrUpdate.CreateOrUpdate(self,data)
			response['result'] = "product successfully updated"
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)

	@classmethod
	@swagger_auto_schema(operation_summary=" Product details by barcode api",query_serializer=ProductByIDSerializer, tags=['Product'])
	def get(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.GET
		data = data.copy()
		data_validation = ProductByIDSerializer(data=data)
		is_valid_data = data_validation.is_valid()
		if is_valid_data:
			data = data_validation.validated_data
			barcode = data.get("barcode")
			product = Product.objects.select_related('brand').filter(
				item_code=barcode,
				store_id=store_id,
				isactive=True,
				isdeleted=False
			)
			if product.last():
				obj = ProductInfo.Details(self,product)
				response["data"] = obj
			else:
				status_code = 400
				response["errors"] = "Invalid Barcode"
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)

	@classmethod
	@swagger_auto_schema(operation_summary=" Product status change api",request_body=ProductStatusChangeSerializer, tags=['Product'])
	def patch(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.data
		data = data.copy()

		data_validation = ProductStatusChangeSerializer(data=data)
		is_valid_data = data_validation.is_valid()
		if is_valid_data:
			data = data_validation.validated_data
			product_ids = data.get("product_ids")
			status = data.get("status")
			deals = data.get("deals",None)
			if status == "true":
				status = True
			if status == "false":
				status = False
			product_ids = product_ids.split(",")
			product_ids = [int(x)for x in product_ids]
			if deals:
				product = Product.objects.filter(
					id__in=product_ids,
					isactive=True
				).update(**{deals:status})
			else:
				product = Product.objects.filter(
					id__in=product_ids,
				).update(isactive=status)
			status_code = 200
			status_name = "Inactive"
			if status:
				status_name = "Active"
			response["message"] = "Product successfully "+status_name
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)

	@classmethod
	@swagger_auto_schema(operation_summary=" Product delete api",query_serializer=ProductChangeSerializer, tags=['Product'])
	def delete(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.GET
		data = data.copy()

		data_validation = ProductChangeSerializer(data=data)
		is_valid_data = data_validation.is_valid()
		if is_valid_data:
			data = data_validation.validated_data
			product_ids = data.get("product_ids")
			status = data.get("status")
			product_ids = product_ids.split(",")
			product_ids = [int(x)for x in product_ids]
			product = Product.objects.filter(
				id__in=product_ids,
				store_id=store_id
			).update(isactive=False,isdeleted=True)
			status_code = 200
			response["message"] = "Product successfully Deleted"
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)


class ProductListView(GenericAPIView):
	"""
		 product List api
	"""
	serializer_class = ProductListSerializer
	permission_classes = [IsAuthenticated]

	@classmethod
	@swagger_auto_schema(operation_summary=" Product List",query_serializer=ProductListSerializer,tags=['Product'])
	def get(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.GET
		data = data.copy()
		data.update({
			"user_id":request.user.id
		})
		
		data_validation = ProductListSerializer(data=data)
		is_valid_data = data_validation.is_valid()

		if is_valid_data:
			data = data_validation.validated_data
			category_id = data.get('category_id')
			category_name = data.get('category_name')
			limit = data.get("limit")
			status = data.get("status")
			page = data.get("page")
			deals = data.get("deals")
			order = data.get("order")
			search_text = data.get("search", "")
			lookup = data.get("lookup",False)
			fields = [
					"id","name"
				]
			if deals:
				fields.extend(
					[
						"onhand_stock","price"
					]
				)
				fields.append(deals)
			elif not lookup:
				fields.extend(
						[
							"brand_name","price","onhand_stock","description","item_code","pack",
							"case_till","case_max","special_quantity","special_price","updated_date",
							"special_pack_bulk","special_from","special_till","special_max","created_date","image",
							"size","product_unit","tax","discount","isactive","category_name",
						]
					)
			"""This is comment # order = getorderColumn(order,fields)""" 
			offset = (page - 1) * limit
			newLimit = (page * limit)
			"""
				query to get product list
			"""
			filterquery = Q(
				isdeleted=False,
			)
			if category_id:
				if not category_id.isdigit():
					multiple_category_id = [int(cid) for cid in category_id.split(',')]
					filterquery.add(
						Q(category_id__in=multiple_category_id),
						Q.AND
					)
				else:
					category_id1 = int(category_id)
					filterquery.add(
						Q(category_id=category_id1),
						Q.AND
					)
				
			if category_name:
				category_name1 = category_name
				filterquery.add(
					Q(category__name__icontains=category_name1),
					Q.AND
				)

			if deals:
				filterquery.add(
					Q(isactive=True),
					Q.AND
				)
				mystatus = False
				if status == "true":
					mystatus = True
				if status !="all":
					filterquery.add(
						Q(**{deals: mystatus}),
						Q.AND
					)
			else:
				if status == "true":
					filterquery.add(
						Q(isactive=True),
						Q.AND
					)
				elif status == "false":
					filterquery.add(
						Q(isactive=False),
						Q.AND
					)
			print(filterquery)
			pro_list = Product.objects.filter(
				filterquery
			)
			if search_text:
				item_code_pro_list = pro_list.filter(item_code__exact=search_text)
				if item_code_pro_list:
					pro_list=item_code_pro_listm 
				else:
					pro_list = pro_list.filter(Q(name__icontains=search_text))
			total = pro_list.count()
			res= pro_list.annotate(
				category_name=ArrayAgg(F('category__name')),
			).values(*fields).order_by(*order)[offset:newLimit]
			
			response["result"] = res
			response["length"]= len(res)
			response["total"] = total
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)

class SaleCountUpdateView(GenericAPIView):
	"""
	API view to update the sale count of products.
	"""
	permission_classes = [IsAuthenticated]
	serializer_class = SaleCountUpdateSerializer

	@swagger_auto_schema(
		operation_summary="Update sale count for products",
		request_body=SaleCountUpdateSerializer,
		tags=['Product']
	)
	def patch(self, request, *args, **kwargs):
		data = request.data
		serializer = self.get_serializer(data=data)
		
		if serializer.is_valid():
			product_id = data.get("product_id")
			product_count = data.get("product_count")

			products = Product.objects.filter(id=product_id)

			if not products.exists():
    			status_code = 400
				response["errors"] = "Invalid Barcode"
			else:
				status_code = 400
				products.update(sale_count=product_count)
				response["message"] = "Count updated succesfully"

		return Response(response, status=status_code)

