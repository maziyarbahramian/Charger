"""
URL mapping for the user API.
"""
from django.urls import path
from seller import views

app_name = 'seller'

urlpatterns = [
    path('create/', views.CreateSellerView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
