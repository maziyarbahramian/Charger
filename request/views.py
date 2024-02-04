from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from request import serializers
from request.services import RequestService
from core.models import (
    CreditRequest
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
