from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name = "entry"),
    path("Create New Page", views.create, name = "create"),
    path("edit/<str:title>", views.edit, name = "edit"),
    path("random", views.random, name = "random"),
    path("search", views.search, name = "search")
]
