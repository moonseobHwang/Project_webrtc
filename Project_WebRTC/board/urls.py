

from django.contrib import admin
from django.urls import path, include

from . import views

app_name='board'

urlpatterns = [
    path('', views.list),
    path('list/', views.list, name="list"),
    path('view/<int:id>/<int:page>', views.view, name="view"),
    path('delete/<int:id>/', views.delete, name="delete"),      # view 페이지에서 개별 삭제를 위한 path
    path('delete/', views.delete, name="delete"),   # list 페이지에서 일괄삭제를 위한 path
    path('search/', views.search, name="search"),
]