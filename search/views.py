#
#   file 	: search/views.py
#	author	: andromeda
#   desc 	: Model parsing and variable retrieval for each search app URL controller
#
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
	template_name = "search/view.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SearchProductView, self).get_context_data(*args, **kwargs)
    #     query = self.request.GET.get('q')
    #     context['query'] = query
    #     return context

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_data(*args, **kwargs)
		query = self.request.GET.get('q')
		context['query'] = query
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		method_dict = request.GET
		query = method_dict.get('q', None)      # every method dict had a 'get' call function
		if query is not None:
		    return Product.objects.search(query)
		return Product.objects.featured()

		'''
		__icontains = field contains this
		__iexact = fields is exactly this

		'''
