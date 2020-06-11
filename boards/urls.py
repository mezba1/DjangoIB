from django.urls import path

from . import views


urlpatterns = [
    path('<slug:slug>/', views.board_index, name='dib-board-index'),
    path('<slug:slug>/archive/', views.catalog_index, name='dib-archive-index'),
    path('<slug:slug>/catalog/', views.catalog_index, name='dib-catalog-index'),
    path('<slug:slug>/<int:page>/', views.board_index, name='dib-board-index-page'),
    path('<slug:slug>/thread/<int:thread_id>/', views.thread_index, name='dib-thread-index'),
    path('', views.index, name='dib-index'),
]
