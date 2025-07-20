from rest_framework.viewsets import ModelViewSet
from ..models.loan import Loan
from ..serializers.loan import LoanSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django.utils import timezone

class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.select_related('book').all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        return Loan.objects.select_related('book').all()
    
    @extend_schema(
        request=None,
        responses={
            200: LoanSerializer,
            400: {'description': 'Error: El préstamo ya ha sido devuelto'}
        }
    )
    @action(detail=True, methods=['post'], url_path='return')
    def return_loan(self, request, pk=None):
        loan = self.get_object() 
        if loan.return_date:
            return Response(
                {'error': 'El préstamo ya ha sido devuelto'},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.return_date = timezone.now().date()
        loan.save()
        loan.book.is_available = True
        loan.book.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)