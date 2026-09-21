import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def get_book_info(isbn):
    try:
        response = requests.get(
            f'{settings.OPENLIBRARY_API_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data',
            timeout=settings.OPENLIBRARY_TIMEOUT
        )

        response.raise_for_status()

    except requests.Timeout:
        logger.warning("API : délai d'attente dépassé pour l'ISBN %s", isbn)
        return None

    except requests.RequestException as exc:
        logger.warning("API : requête en échec pour l'ISBN %s (%s)", isbn, exc)
        return None

    try:
        data = response.json()

    except ValueError:
        logger.warning(
            "API :réponse illisible pour l'ISBN %s", isbn)
        return None

    book = data.get(f'ISBN:{isbn}')

    if book is None:
        return None

    authors = book.get('authors', [])
    publishers = book.get('publishers', [])
    cover = book.get('cover', {})

    return {
        'title': book.get('title', ''),
        'author': authors[0].get('name', '') if authors else '',
        'publisher': publishers[0].get('name', '') if publishers else '',
        'publish_year': book.get('publish_date', ''),
        'cover_url': cover.get('medium', '')
    }