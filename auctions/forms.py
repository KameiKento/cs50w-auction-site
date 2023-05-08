from django import forms
from .models import Auction
from .models import Bid, Comment, WatchList


class AuctionForm(forms.ModelForm):
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


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["auction", "bidder", "amount"]
        widgets = {
            "auction": forms.HiddenInput(),
            "bidder": forms.HiddenInput(),
        }

    def __init__(self, auction, bidder, *args, **kwargs):
        self.auction = auction
        self.bidder = bidder
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        if amount is None or amount <= self.auction.current_bid:
            raise forms.ValidationError("Invalid bid amount")
        return cleaned_data

    def save(self, commit=True):
        bid = super().save(commit=False)
        bid.auction = self.auction
        bid.bidder = self.bidder
        if commit:
            bid.save()
        return bid


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["auction", "user", "text"]
        widgets = {
            "auction": forms.HiddenInput(),
            "user": forms.HiddenInput(),
        }

    def __init__(self, auction, user, *args, **kwargs):
        self.auction = auction
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["auction"].widget = forms.HiddenInput()
        self.fields["user"].widget = forms.HiddenInput()
        self.fields["auction"].initial = auction
        self.fields["user"].initial = user

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.auction = self.auction
        comment.user = self.user
        if commit:
            comment.save()
        return comment
    
class WatchlistForm(forms.ModelForm):
    class Meta:
        model = WatchList
        exclude = ['user', 'auction']
