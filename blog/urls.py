from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('now', views.post_current_time, name='post_current_time'),
]