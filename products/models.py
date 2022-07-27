#
#   file 	: models.py
#	author	: andromeda
#   desc 	: The Product database objects modelling
#
import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator

# filename methods ----------------------------------------------------------------

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1,3248136846)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "products/{new_filename}/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
		)

# models managers -----------------------------------------------------------------

# custom queryset -----------------------------------------------------------------

class ProductQuerySet(models.query.QuerySet):
	def active(self):										# show only active products
		return self.filter(active=True)

	def featured(self):										# show only featured products
		return self.filter(featured=True, active=True)

	def search(self, query):
	    lookups = (Q(title__icontains=query) |
	               Q(description__icontains=query) |
	               Q(price__icontains=query) |
	               Q(tag__title__icontains=query)
	               )
	    return self.filter(lookups)


# main models managers ------------------------------------------------------------

class ProductManager(models.Manager):						# the Product model manager
	def get_queryset(self):									# get the custom queryset
		return ProductQuerySet(self.model, using=self._db)

	def all(self):											# all active product manager
		return self.get_queryset().active()

	def featured(self):										# all featured product manager
		return self.get_queryset().featured()

	def get_by_id(self, id):								# all product manager by id
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None

	def search(self, query):
	    return self.get_queryset().active().search(query)

# models -------------------------------------------------------------------------

class Product(models.Model):
	title		= models.CharField(max_length=120)
	slug		= models.SlugField(blank=True, unique=True)
	description	= models.TextField()
	price		= models.DecimalField(decimal_places=2, max_digits=20, default=30.08)
	image		= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	featured	= models.BooleanField(default=False)
	active		= models.BooleanField(default=True)

	objects 	= ProductManager()

	def get_absolute_url(self):
		return reverse("products:detail", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
