from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_auction, name="create"),
    path("auction/<int:pk>/", views.auction_detail, name="auction_detail"),
    path("comment/<int:pk>/", views.create_comment, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path(
        "auction/<int:pk>/watchlist/add",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
]
