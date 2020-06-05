from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog')
]