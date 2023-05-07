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
]
