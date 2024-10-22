from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, NoteViewSet


router = DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("books", BookViewSet)
router.register("notes", NoteViewSet)

urlpatterns = [
    path("", include(router.urls))
]
