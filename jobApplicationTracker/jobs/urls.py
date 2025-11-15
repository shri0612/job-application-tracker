from django.urls import path
from . import views

# URL patterns for the 'jobs' app
urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('add/', views.add_job, name='add_job'),
    path('<int:id>/edit/', views.edit_job, name='edit_job'),
    path('<int:id>/delete/', views.delete_job, name='delete_job'),
]
