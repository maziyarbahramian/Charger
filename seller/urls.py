"""
URL mapping for the user API.
"""
from django.urls import path, include
from seller import views
from rest_framework.routers import DefaultRouter
app_name = 'seller'

router = DefaultRouter()
router.register('sellers', views.ListSellerViewSet)

urlpatterns = [
    path('create/', views.CreateSellerView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.RetrieveSellerView.as_view(), name='me'),
    path('', include(router.urls)),
]
