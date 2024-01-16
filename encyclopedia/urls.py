from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:search>", views.wiki, name="wiki"),
    path("/search", views.search, name="search"),
    path("/newpage", views.newpage, name="newpage"),
    path("editpage/<str:markdown>", views.editpage, name="editpage"),
    path("randompage/", views.randompage , name="randompage")
]
