from celery import shared_task
import logging
from datetime import timedelta
from django.utils.timezone import now
from .models import Book


logger = logging.getLogger(__name__)


@shared_task
def archive_old_books():
    ten_years_ago = now().date() - timedelta(days=10*365)
    books = Book.objects.filter(
        published_date__lt=ten_years_ago, is_archived=False)
    books.update(is_archived=True)


@shared_task
def log_book_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Book created: {instance.title} by {instance.author}")
        print(f"Book created: {instance.title} by {instance.author}")


@shared_task
def get_books(sender, **kwargs):
    print("Fetching books...")
