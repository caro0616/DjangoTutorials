from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django.core.exceptions import ValidationError

# Página de inicio
def homePageView(request):
    return render(request, 'pages/home.html')

# Vista basada en clase para home
class HomePageView(TemplateView):
    template_name = 'home.html'

# Página "About"
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page",
            "author": "Developed by: Kenia Toscano",
        })
        return context

# Clase simulada para productos (sin base de datos)
class Product:
    products = [
        {"id": 0, "name": "TV", "price": 468.99},
        {"id": 1, "name": "iPhone", "price": 897.99},
        {"id": 2, "name": "Chromecast", "price": 49.99},
        {"id": 3, "name": "Glasses", "price": 79.99},
    ]

    @staticmethod
    def get_by_id(product_id):
        for product in Product.products:
            if product["id"] == product_id:
                return product
        return None

# Vista para listar productos
class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products
        }
        return render(request, self.template_name, viewData)

# Vista para mostrar un producto
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            id = int(id)
        except ValueError:
            return HttpResponseRedirect(reverse('home'))

        product = Product.get_by_id(id)
        if not product:
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)

# Formulario para crear productos
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than 0.")
        return price

# Vista para crear un producto
class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            viewData = {
                "title": "Product Created"
            }
            return render(request, 'products/created.html', viewData)
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)

