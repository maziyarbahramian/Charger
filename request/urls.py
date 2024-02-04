from django.urls import path
from request import views

urlpatterns = [
    path('credit-request',
         views.CreateCreditRequestViewSet.as_view(),
         name='credit-request'),
]
