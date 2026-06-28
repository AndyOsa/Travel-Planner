from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('projects/<int:project_pk>/places/', views.place_list, name='place-list'),
    path('projects/<int:project_pk>/places/<int:place_pk>/', views.place_detail, name='place-detail'),
]