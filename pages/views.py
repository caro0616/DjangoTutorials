from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Página de inicio (function-based, opcional)
def homePageView(request):
    return render(request, 'pages/home.html')

# Vista basada en clase para home
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


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


# Vista para listar productos (usando View)
class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)


# Vista para mostrar un único producto
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # Validar si el ID es un entero positivo
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError()
        except (ValueError, TypeError):
            return HttpResponseRedirect(reverse('home'))

        # Obtener el producto o dar 404
        product = get_object_or_404(Product, pk=product_id)

        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)


# Formulario para crear productos con validación de precio
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
            # Aquí no guardas en base de datos porque usas Form, 
            # si lo quisieras, cambias a ModelForm y usas form.save()
            viewData = {"title": "Product Created"}
            return render(request, 'products/created.html', viewData)
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)


# Vista genérica para listar productos usando ListView
class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context
