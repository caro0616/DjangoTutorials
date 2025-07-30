from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# Vista para la página de inicio
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Home - Online Store",
            "subtitle": "Welcome to the application",
            "description": "This is the home page ...",
            "author": "Developed by: Leidy Obando",
        })
        return context

# Vista para la página "about"
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Leidy Obando",
        })
        return context

# Clase simulada de productos (con precios)
class Product:
    products = [
        {
            "id": "tv",
            "name": "TV",
            "description": "Smart TV 55 pulgadas 4K UHD",
            "price": 800
        },
        {
            "id": "iphone",
            "name": "iPhone",
            "description": "iPhone 14 Pro Max 256GB",
            "price": 1200
        },
        {
            "id": "chromecast",
            "name": "Chromecast",
            "description": "Chromecast con Google TV",
            "price": 50
        },
        {
            "id": "glasses",
            "name": "Smart Glasses",
            "description": "Gafas inteligentes de realidad aumentada",
            "price": 300
        },
    ]

    @classmethod
    def find_by_id(cls, id):
        return next((product for product in cls.products if product["id"] == id), None)


# Vista para mostrar todos los productos
class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products
        }
        return render(request, self.template_name, viewData)

# Vista para mostrar un solo producto por ID
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        product = Product.find_by_id(id)
        if not product:
            return HttpResponseRedirect('/')  # redirección si no existe

        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)
