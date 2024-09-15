from django.urls import path
from product_management import views

urlpatterns = [

	path(
		"product",
		views.ProductView.as_view(),
		name="_product_view"
	),
	path(
		"product-list",
		views.ProductListView.as_view(),
		name="_product_list_view"
	),
	path(
		'update-sale-count/',
		views.SaleCountUpdateView.as_view(), 
		name='update-sale-count'
	),
	
]