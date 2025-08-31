# adminpanel/forms.py
from django import forms
from shop.models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'image': forms.FileInput(attrs={'class': 'w-full'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'description', 'is_available', 'is_featured', 'price']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'image': forms.FileInput(attrs={'class': 'w-full'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
        }
