from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book, Note
from .serializers import AuthorSerializer, BookSerializer, NoteSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related(
        Prefetch('books', queryset=Book.objects.all())).all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author__name', 'genre', 'published_date']
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60), name="list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.clear()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.clear()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.clear()


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-id')
    serializer_class = NoteSerializer
