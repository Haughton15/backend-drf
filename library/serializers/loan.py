from datetime import date
from ..models.loan import Loan
from rest_framework.serializers import ModelSerializer, ValidationError

class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'book', 'borrower_name', 'loan_date', 'return_date']
        read_only_fields = ['loan_date', 'return_date']

    def create(self, validated_data):
        validated_data['loan_date'] = date.today()
        book = validated_data['book']

        if not book.is_available:
            raise ValidationError("El libro no está disponible para préstamo.")

        book.is_available = False
        book.save()
        return super().create(validated_data)
    
class ReturnLoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'return_date']

    def update(self, instance):
        if instance.return_date:
            raise ValidationError("Este préstamo ya fue devuelto.")

        instance.return_date = date.today()
        instance.book.is_available = True
        instance.book.save()
        instance.save()
        return instance