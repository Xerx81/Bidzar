from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("categories", views.show_categories, name="categories"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.close_auctions, name="close_auctions"),
    path("closed_listings", views.closed_listings, name="closed")
]
