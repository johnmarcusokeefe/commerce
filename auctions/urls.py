from django.urls import path

from . import views

#app="auctions"
# without the / in path the page does not route properly
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:filter>", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("watchlist/<str:listing>", views.watchlist, name="watchlist"),
    path("create/", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("endbid/<str:id>", views.endbid, name="endbid")
]
