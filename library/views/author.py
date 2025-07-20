from rest_framework.viewsets import ModelViewSet
from ..models.author import Author
from ..serializers.author import AuthorSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'birth_date': {'type': 'string', 'format': 'date'},
                    'photo': {'type': 'string', 'format': 'binary'},
                },
                'required': ['name', 'birth_date'],
            }
        },
        responses={201: AuthorSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
