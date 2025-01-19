from core.models import Product
from django import forms

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Product title", "class": "form-control"}))
    vendor = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Vendor title", "class": "form-control"}))

    description =  forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Product Description", "class": "form-control" })) 
    price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Sale Price", "class": "form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Old Price", "class": "form-control"}))
    # type = forms.CharField(widget=forms.TimeInput(attrs={"placeholder": "Type of Service e.g Tutor", "class": "form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))
    


    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'digital',
            'category',
            'vendor',
        ]