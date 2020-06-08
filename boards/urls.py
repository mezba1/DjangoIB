from django.urls import path

from . import views


urlpatterns = [
    path('<slug:slug>/', views.slug_view, name='boards-slug'),
    path('<slug:slug>/archive/', views.catalog, name='archive'),
    path('<slug:slug>/catalog/', views.catalog, name='catalog'),
    path('<slug:slug>/<int:page>/', views.slug_view, name='boards-slug-page'),
    path('<slug:slug>/thread/<int:thread_id>/', views.thread_view, name='thread'),
    path('', views.index_view, name='boards-index'),
]
