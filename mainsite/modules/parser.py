import re, urllib2, logging
from ..models import Books

class Parser:
    def ntust_book_page_parser(self, record):
        link = 'http://millennium.lib.ntust.edu.tw/record=%s*cht' % record
        title_ptn = re.compile('\<td class\=\"bibInfoData\"\>\n\<strong\>(.*?)\<\/strong\>\<\/td\>')
        find_number_ptn = re.compile('\<\!\-\- field C \-\-\>\&nbsp\;([\w\-\.\/ ]+)?\<')
        status_ptn = re.compile('\<\!\-\- field \% \-\-\>\&nbsp\;(.*?)\<\/td\>')
        isbn_ptn = re.compile('\<td class\=\"bibInfoData\"\>\n([\d\-]+) ')

        book_page_source = urllib2.urlopen(link).read().decode('utf-8')

        try:
            title = title_ptn.findall(book_page_source)[0].replace('&#59', '')
            find_number = find_number_ptn.findall(book_page_source)[0].rstrip()
            status = status_ptn.findall(book_page_source)[0]
            isbn = isbn_ptn.findall(book_page_source)[0].replace('-', '')
        except:
            logging.info('parse page %s error' % url)
            return None

        book_result = Books.query(Books.link == link).get()
        if book_result == None:
            Books(school='ntust', title=title, link=link, isbn=isbn, find_number=find_number, record=record, status=status).put()
            return isbn
        else:
            return book_result.isbn
