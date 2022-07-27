#
#   file 	: products/views.py
#	author	: andromeda
#   desc 	: Model parsing and variable retrieval for each products app URL controller
#
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product

# CBV Featured List Views -------------------------------------------------------------------------

class ProductFeaturedListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
	queryset = Product.objects.all().featured()
	template_name = "products/featured-detail.html"


# CBV List Views -------------------------------------------------------------------------

class ProductListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all()


# FBV List Views -------------------------------------------------------------------------

def product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset,
	}
	return render(request, "products/list.html", context)

# CBV Detail Views -----------------------------------------------------------------------

class ProductDetailSlugView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Not found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404("Hmm")
		return instance


class ProductDetailView(DetailView):
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		print(context)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product doesn't exist!")
		return instance

# FBV Detail Views -----------------------------------------------------------------------

def product_detail_view(request, pk=None, *args, **kwargs):
	# instance = get_object_or_404(Product, pk=pk)

	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product doesn't exist!")

	context = {
	    'title': 'Test title detail view product',
		'object': instance
	}
	return render(request, "products/detail.html", context)








