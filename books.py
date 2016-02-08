"""Books Recommendations Ranking.

Simple project to fetch books information by ISBN code and arrange them using
a ranking algorithm in a  hubs and authorities' fashion to take in
consideration friend's recommendations for each book, from an external api, and
personal from the book's review.

Wicho Valdeavellano
Feb 2016
"""

import requests
import csv
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
        raise KeyError("Book not found by ISBN %s" % isbn)
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
    book.num_pages = root.find('num_pages').text
    book.num_pages = int(book.num_pages) if book.num_pages is not None else 0
    book.pub_year = int(work.find('original_publication_year').text)
    book.description = root.find('description').text
    book.author = root.find('authors')[0].find('name').text
    book.isbn = isbn
    return book


def generate_books_csv(file_name, out_name="books_info.csv"):
    """Read ISBNs from csv and generate csv with books info."""
    books = []
    with open(file_name, encoding='utf-8') as input_file:
        csv_reader = csv.reader(input_file)
        csv_reader.__next__()
        for row in csv_reader:
            try:
                b = get_book_by_isbn(row[1])
            except KeyError:
                print("ERROR: Book not found (%s)" % row[0])
                continue
            print(b.title)
            books.append(b)

    print("\nBegin writing...\n")
    with open(out_name, 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "ISBN",
            "Title",
            "Author",
            "Original Title",
            "Publication Year",
            "Description",
        ])
        for book in books:
            csv_writer.writerow([
                book.isbn,
                book.title,
                book.author,
                book.original_title,
                book.pub_year,
                book.description,
            ])

if __name__ == '__main__':
    # b = get_book_by_isbn(9780143106531)
    # print(
    #     b.id,
    #     b.title,
    #     b.author,
    #     b.original_title,
    #     b.external_rating,
    #     b.external_rating_count,
    #     b.num_pages,
    #     b.pub_year,
    #     b.description,
    #     sep='\n'
    # )
    generate_books_csv("isbns.csv")
