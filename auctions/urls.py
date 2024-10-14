from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login",  views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing', views.listing, name='listing'),
    path("listing/addlisting", views.addListing, name="addListing"),
    path('listing/<int:listing_id>/closeBid', views.closeBid, name='closeBid' ),
    path('<int:listing_id>/show', views.showList, name='shows'),
    path('<int:listing_id>/addBid', views.addBid, name='addBid'),
    path('<int:listing_id>/comment', views.addComment, name='addComment'),
    path('watchlist', views.showWatchlist, name='watchlist'),
    path('watchlist/<int:listing_id>/add', views.removeWatchlist, name='removeWatchlist'),
    path('watchlist/<int:listing_id>/remove', views.addWatchlist, name='addWatchlist')
]
