# adminpanel/forms.py
from django import forms
from shop.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#BDA78B]',
                'placeholder': 'Category name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Make image optional for updates


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'description', 'price', 'is_available', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#BDA78B]',
                'placeholder': 'Product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded h-24 resize-none focus:outline-none focus:ring-2 focus:ring-[#BDA78B]',
                'placeholder': 'Description',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#BDA78B]',
                'placeholder': 'Price (₹)',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Make image optional for updates
        self.fields['category'].widget = forms.HiddenInput()  # Category is set via JS