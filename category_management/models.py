from django.db import models

class Category(models.Model):
	name = models.CharField(
		max_length=255,
		null=True,
		blank=True
	)
	icon = models.CharField(
		max_length=255,
		null=True,
		blank=True
	)
	image = models.TextField(
		null=True,
		blank=True
	)
	cat_order = models.IntegerField(
		default=0
	)
	slug = models.SlugField(
		max_length=255,
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
