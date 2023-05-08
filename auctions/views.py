from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction, Comment, Bid, WatchList
from .forms import AuctionForm, BidForm, CommentForm, WatchlistForm
from datetime import datetime
from django.contrib import messages

from django.shortcuts import render
from django.utils import timezone


def index(request):
    auctions = Auction.objects.filter(end_time__gt=timezone.now())
    return render(request, "auctions/index.html", {"auctions": auctions})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.start_time = timezone.now()
            auction.save()
            return redirect("auction_detail", pk=auction.pk)
    else:
        form = AuctionForm(initial={"start_time": datetime.now()})
    return render(request, "auctions/create_auction.html", {"form": form})


@login_required
def auction_detail(request, pk):
    # オークションを取得する
    auction = get_object_or_404(Auction, pk=pk)

    # オークションに対するコメントを取得する
    comments = Comment.objects.filter(auction=auction)

    # オークションに対する入札を取得する
    bids = Bid.objects.filter(auction=auction)

    if request.method == "POST":
        bid_form = BidForm(
            auction=auction,
            bidder=request.user,
            data=request.POST,
            initial={"bidder": request.user, "auction": auction},
        )
        if bid_form.is_valid():
            bid_form.save()
            return redirect("auction_detail", pk=pk)

    elif request.method == "GET" and request.GET.get("close_auction"):
        if auction.owner == request.user:
            auction.close()
            messages.success(request, "Auction closed successfully!")
            return redirect("index")

    else:
        bid_form = BidForm(
            auction=auction,
            bidder=request.user,
            initial={"bidder": request.user, "auction": auction},
        )

    # テンプレートコンテキストを作成する
    context = {
        "auction": auction,
        "comments": comments,
        "bids": bids,
        "bid_form": bid_form,
        "user": request.user,
        "pk": pk,
    }

    if not bid_form.is_valid() and bid_form.errors.get("amount"):
        context["error_message"] = bid_form.errors["amount"][0]

    # オークション詳細テンプレートをレンダリングする
    return render(request, "auctions/auction_detail.html", context=context)


def create_comment(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(
            auction=auction,
            user=request.user,
            data=request.POST,
            initial={"user": request.user, "auction": auction},
        )

        if comment_form.is_valid():
            comment_form.save()
            return redirect("auction_detail", pk=pk)

    comment_form = CommentForm(auction=auction, user=request.user)
    return render(request, "auctions/add_comment.html", {"comment_form": comment_form})


@login_required
def add_to_watchlist(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if request.method == "POST":
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist_item = form.save(commit=False)
            watchlist_item.user = request.user
            watchlist_item.auction = auction
            watchlist_item.save()
            return redirect("auction_detail", pk=pk)
    else:
        form = WatchlistForm()

    return render(
        request, "auctions/watchlist_add.html", {"form": form, "auction": auction}
    )


@login_required
def watchlist(request):
    auctions = request.user.watchlists.all()
    return render(request, "auctions/watchlist.html", {"auctions": auctions})


@login_required
def remove_from_watchlist(request):
    if request.method == "POST":
        auction_id = request.POST.get("auction_id")
        if auction_id:
            try:
                auction = Auction.objects.get(pk=auction_id)
                watchlist_item = WatchList.objects.get(
                    user=request.user, auction=auction
                )
                watchlist_item.delete()
                messages.success(
                    request, f"{auction.name} was removed from your watchlist."
                )
            except (Auction.DoesNotExist, WatchList.DoesNotExist):
                messages.error(
                    request,
                    "The selected item could not be removed from your watchlist.",
                )
        else:
            messages.error(request, "Invalid request, please try again.")
    return redirect("watchlist")
