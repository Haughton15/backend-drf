from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from ..models.loan import Loan
from ..serializers.loan import LoanSerializer, ReturnLoanSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.select_related('book').all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        return Loan.objects.select_related('book').all()
    
class ReturnLoanAPIView(APIView):
    def post(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        serializer = ReturnLoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Libro devuelto correctamente'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)