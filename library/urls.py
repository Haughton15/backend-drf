from django.urls import path
from rest_framework.routers import DefaultRouter
from library.views.author import AuthorViewSet
from library.views.books import BookViewSet
from library.views.loan import LoanViewSet, ReturnLoanAPIView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = router.urls + [
    path('loans/<int:pk>/return/', ReturnLoanAPIView.as_view(), name='loan-return'),
]
