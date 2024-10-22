from rest_framework import serializers
from .models import Author, Book, Note


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField(method_name="get_books")

    class Meta:
        model = Author
        fields = "__all__"

    def get_books(self, obj):
        return BookListSerializer(obj.books.all(), many=True).data


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
