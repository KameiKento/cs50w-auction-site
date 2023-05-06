from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass


class Auction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="won_auctions",
    )
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(upload_to="auction_images/", null=True, blank=True)

    def __str__(self):
        return self.name

    def update_current_bid(self, bid_amount):
        if bid_amount >= self.starting_bid:
            self.current_bid = bid_amount
        else:
            self.current_bid = self.starting_bid
        self.save()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.auction}"

    def clean(self):
        if self.bidder == self.auction.owner:
            raise ValidationError("Owner cannot bid on their own auction.")
        if (
            self.auction.current_bid is not None
            and self.amount <= self.auction.current_bid
        ):
            raise ValidationError("Bid must be higher than the current bid.")
        elif not self.auction.current_bid and self.amount < self.auction.starting_bid:
            raise ValidationError(
                "Bid amount must be greater than or equal to the starting bid."
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.auction.update_current_bid(self.amount)
        super().save(*args, **kwargs)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.user} commented on {self.auction}"
