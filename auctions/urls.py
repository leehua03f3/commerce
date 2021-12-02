from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("listing/<int:item_id>/bidding", views.bidding, name="bidding"),
    path("listing/<int:item_id>/watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:item_id>/close_bid", views.close_bid, name="close_bid"),
    path("listing/<int:item_id>/comment", views.comment, name="comment"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("category", views.category, name="category"),
    path("category/<str:name>", views.category_name, name="category_name")
]
