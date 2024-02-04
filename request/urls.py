from django.urls import path
from request import views

urlpatterns = [
    path('credit-request',
         views.CreateCreditRequestViewSet.as_view(),
         name='credit-request'),
    path('accept-credit-request',
         views.AcceptCreditRequestViewSet.as_view(),
         name='accept-credit-request'),

]