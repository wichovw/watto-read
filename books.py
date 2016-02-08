"""Books Recommendations Ranking.

Simple project to fetch books information by ISBN code and arrange them using
a ranking algorithm in a  hubs and authorities' fashion to take in
consideration friend's recommendations for each book, from an external api, and
personal from the book's review.

Wicho Valdeavellano
Feb 2016
"""

import requests
import xml.etree.ElementTree as et

goodreads_api_key = '6dy1cjEh711lOz2KHqYryg'


class Book:
    """Describes a book entity."""

    pass


def get_book_by_isbn(isbn):
    """Return a book object by its ISBN code."""
    rsp = requests.get(
        'https://www.goodreads.com/book/isbn?format=xml&isbn=%s&key=%s' %
        (isbn, goodreads_api_key)
    )
    if rsp.status_code != 200:
        raise KeyError
    root = et.fromstring(rsp.text).find('book')
    book = Book()
    book.id = int(root.find('id').text)
    work = root.find('work')
    book_best_id = int(work.find('best_book_id').text)

    if book.id != book_best_id:
        rsp = requests.get(
            'https://www.goodreads.com/book/show.xml?id=%s&key=%s' %
            (book_best_id, goodreads_api_key)
        )
        root = et.fromstring(rsp.text).find('book')
        book.id = book_best_id

    book.title = root.find('title').text
    book.original_title = work.find('original_title').text
    book.external_rating = float(root.find('average_rating').text)
    book.external_rating_count = int(work.find('ratings_count').text)
    book.num_pages = int(root.find('num_pages').text)
    book.pub_year = int(work.find('original_publication_year').text)
    book.description = root.find('description').text
    book.author = root.find('authors')[0].find('name').text
    return book

if __name__ == '__main__':
    b = get_book_by_isbn(9780307472595)
    print(
        b.id,
        b.title,
        b.author,
        b.original_title,
        b.external_rating,
        b.external_rating_count,
        b.num_pages,
        b.pub_year,
        b.description,
        sep='\n'
    )
