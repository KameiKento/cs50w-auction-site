from django.contrib import admin
from .models import Auction, Bid, Comment, WatchList


class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "start_time",
        "end_time",
        "starting_bid",
        "current_bid",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "user", "text")
    list_filter = ("auction", "user")


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList)
