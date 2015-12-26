import urllib2, re, logging
from ..models import UserTraceBooks, Books

class BookRelated:
    def add_trace_book(self, isbn):
        UserTraceBooks(isbn=isbn).put()
        logging.info('add %s' % isbn)

    def remove_trace_book(self, isbn):
        db_record = UserTraceBooks.query(UserTraceBooks.isbn==isbn).get()
        db_record.key.delete()
        logging.info('remove %s' % isbn)

    def get_trace_books(self):
        trace_books = UserTraceBooks.query().fetch()
        for trace_book in trace_books:
            book_info = Books.query(Books.isbn == trace_book.isbn).get()
            if book_info != None:
                trace_book.title = book_info.title
                trace_book.status = book_info.status
                trace_book.find_number = book_info.find_number
            else:
                trace_book.title = None
                trace_book.status = None
                trace_book.find_number = None

        return trace_books

    def update_book_status(self):
        update_count = 0
        status_ptn = re.compile('\<\!\-\- field \% \-\-\>\&nbsp\;(.*?)\<\/td\>')
        trace_books = UserTraceBooks.query().fetch()
        for trace_book in trace_books:
            book_info = Books.query(Books.isbn == trace_book.isbn).get()
            book_page_source = urllib2.urlopen(book_info.link).read().decode('utf-8')
            status = status_ptn.findall(book_page_source)[0]

            if status != book_info.status:
                book_info.status = status
                book_info.put()
                update_count = update_count + 1

        logging.info('update %s book status' % update_count)
