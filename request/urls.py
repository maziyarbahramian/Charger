from django.urls import path, include
from request import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('credit-request', views.CreditRequestViewSet)
router.register('transaction', views.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('credit-request',
         views.CreateCreditRequestViewSet.as_view(),
         name='credit-request'),
    path('accept-credit-request',
         views.AcceptCreditRequestViewSet.as_view(),
         name='accept-credit-request'),
    path('reject-credit-request',
         views.RejectCreditRequestViewSet.as_view(),
         name='reject-credit-request'),
    path('charge-phone-number',
         views.ChargePhoneNumberViewSet.as_view(),
         name='charge-phone-number'),
]
