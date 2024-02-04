from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from request import serializers
from request.services import RequestService


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
