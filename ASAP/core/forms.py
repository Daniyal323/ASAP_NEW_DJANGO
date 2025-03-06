from django import forms 
from core.models import ProductReview, Seller

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs = {'placeholder': "Write review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

class SellerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['business_name', 'business_address', 'phone']
