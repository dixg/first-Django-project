from django.urls import path
import markdown2
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.display_entry, name="display"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage")
]
