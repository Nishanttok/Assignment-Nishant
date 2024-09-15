from rest_framework.generics import GenericAPIView
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser
from admins.file_import_management.create_or_update import check_boolean
from customer.models import *
from customer.common.views import *
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.conf import settings
import os
import re
from django.utils import timezone
from pathlib import Path
class AdminProductCreateOrUpdate(GenericAPIView):
	@staticmethod
	def CreateOrUpdate(self,row):
		currentdattime = timezone.now()

		bulkInsert_data=[]
		bulkUpdate_data=[]
		product_data=[]
		pro_cat_data=[]
		pro_cam_data=[]
		slug_data=[]
		item_code_data=[]

		img_dict = {}
		special_from = row.get("special_from")
		special_till = row.get("special_till")
		if special_from:
			special_from = str(dateformat(special_from,start=True))
		if special_till:
			special_till = str(dateformat(special_till,start=True))

		if special_from and special_till:
			is_special_date_check=True
		else:
			is_special_date_check=False



		available_on_days=""
		available_on_days_data=row.get("available_on_days")
		if available_on_days_data:
			mystr = row.get("available_on_days")
			available_data = re.findall(r'\d+(?:,\d+)?',mystr)
			available_on_days= ",".join(available_data)


		slug = slugify(row.get('description').strip())
		pro_in_crr_arr = -1
		if slug in slug_data:
			pro_in_crr_arr = next((index for (index, d) in enumerate(product_data) if d.item_id == row.get('item_code')), -1)
			slug = slugify(row.get('description').strip() +"-"+str(row.get('item_code')))
		slug_data.append(slug)
		item_code_data.append(str(row.get('item_code')).strip())

		""" based on condition """
		product_ins=None
		product = Product.objects.filter(
			item_code=str(row.get('item_code')).strip()
		)
		if product.last():
			product_ins = product.last()
        else:
            product_ins = Product.objects.create(
                item_code=str(row.get('item_code')).strip()
            )

		images_data = ""
		img1= row.get("image1").strip() if row.get("image1") else None
		if img1:
			images_data = img1

		pack_data=1
		if row.get("pack") and str(row.get("pack")).isdigit():
			pack_data= row.get("pack")
			
		
		if not product:
			product_ins = Product.objects.create(
				item_code=str(row.get('item_code')).strip()
			)

		if product_ins:
			bulkUpdate_data.append(obj)
			product_ins.slug=slug
			product_ins.name= row.get("description").strip()
			
			
			product_ins.item_code=row.get("item_code").strip()
			product_ins.brand_id = brand.id if brand else None
			product_ins.pack=pack_data
			product_ins.price=row.get("price")
			product_ins.special_quantity=row.get("special_quantity")
			product_ins.special_price=row.get("special_price")
			product_ins.special_pack_bulk=row.get("special_pack_bulk")
			product_ins.special_from=special_from
			product_ins.special_till=special_till

			product_ins.is_special_date_check=is_special_date_check

			product_ins.special_max=row.get("special_max")
			product_ins.onhand_stock=row.get("onhand_stock")
			product_ins.size=row.get("size")
			product_ins.product_unit=row.get("product_unit")

			product_ins.is_by_weight=row.get("is_by_weight")

			product_ins.tax=row.get("tax")
			product_ins.discount=row.get("discount")

			product_ins.image=images_data
			
			product_ins.today_deals=row.get("today_deal")
			product_ins.popular_products=row.get("popular_products")

			product_ins.isactive=row.get("isactive")
			product_ins.updated_date=currentdattime
			product_ins.isdeleted=False
			product_ins.save()

			return True