from django import forms
from django.forms import ModelForm
from .models import Auction


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            "name",
            "description",
            "start_time",
            "end_time",
            "starting_bid",
            "image_url",
            "category",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    image_url = forms.URLField(max_length=200, required=False)
