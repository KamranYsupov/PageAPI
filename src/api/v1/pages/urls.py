from django.urls import path
from . import views

urlpatterns = [
    path('', views.PageList.as_view(), name='page-list'),
    path('<int:pk>/', views.PageDetail.as_view(), name='page-detail'),
]

