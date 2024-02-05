from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from request import serializers
from request.services import RequestService
from core.models import (
    CreditRequest,
    Seller,
    Transaction
)


class CreateCreditRequestViewSet(generics.GenericAPIView):
    serializer_class = serializers.CreateCreditRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        service = RequestService()
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.validated_data
            seller_id = valid_data['seller_id']
            amount = valid_data['amount']

            credit_request = service.create_credit_request(
                seller_id, amount)
            output_serializer = self.serializer_class(credit_request)
            return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class AcceptCreditRequestViewSet(generics.GenericAPIView):
    serializer_class = serializers.AcceptCreditRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        service = RequestService()
        if serializer.is_valid(raise_exception=True):
            request_id = serializer.validated_data['request_id']
            try:
                transaction = service.accept_credit_request(request_id)
            except CreditRequest.AlreadyProcessedError:
                response = {
                    'error': 'Process already completed.',
                    'message': 'The requested process has already been done. Subsequent requests are not allowed.'
                }
                return Response(data=response, status=status.HTTP_409_CONFLICT)
            output_serializer = self.serializer_class(transaction)
            return Response(output_serializer.data)


class CreditRequestViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = serializers.CreditRequestSerializer
    queryset = CreditRequest.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return CreditRequest.objects.filter(seller=self.request.user)
        else:
            return self.queryset


class ChargePhoneNumberViewSet(generics.GenericAPIView):
    serializer_class = serializers.ChargePhoneNumberSerializer
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        service = RequestService()
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data['phone_number']
            amount = serializer.validated_data['amount']
            try:
                transaction = service.charge_phone_number(
                    request.user.id, phone_number, amount
                )
                output_seralizer = self.serializer_class(transaction)
                return Response(data=output_seralizer.data, status=status.HTTP_200_OK)

            except Seller.InsufficientCreditError:
                response = {
                    'error': 'Insufficient credit.',
                    'message': 'The requested process requires more credit than available.'
                }
                return Response(data=response, status=status.HTTP_402_PAYMENT_REQUIRED)
