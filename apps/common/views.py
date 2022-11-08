from django.shortcuts import render

# Create your views here.

bredcrumbs = [ {"name": "Dashboard", "url": "/dashboard/"}, {"name": "Settings", "url": "/settings/"} ]
class breadcrumb:
	def __init__(self, name, url):
		self.name = name
		self.url = url
	
