#!/usr/bin/python
# -*- coding: utf8 -*-

import urllib2, re, logging
from ..models import Library, Books

class CronJobRelated:
    def rss_update(self, school_name):
        library_result = Library.query(Library.school_name == school_name).get()
        if library_result.school_name == 'ntust':
            self.ntust_parser(library_result)
        return

    def ntust_parser(self, library_result):
        parse_count = success_count = failed_count = 0
        item_ptn = re.compile('\<item\>(.*?)\<\/item\>', re.DOTALL)
        title_ptn = re.compile('\<title\>(.*?)\<\/title\>')
        link_ptn = re.compile('\<link\>(.*?)\<\/link\>')
        find_number_ptn = re.compile('\<\!\-\- field C \-\-\>\&nbsp\;([\w\-\.\/ ]+)?\<')
        status_ptn = re.compile('\<\!\-\- field \% \-\-\>\&nbsp\;(.*?)\<\/td\>')
        isbn_ptn = re.compile('\<guid isPermaLink\=\"false\"\>([\d\-]+)')
        record_ptn = re.compile('record\=(\w+)\*')

        rss_page_source = urllib2.urlopen(library_result.rss_url).read().decode('utf-8')
        items = item_ptn.findall(rss_page_source)
        for item in items:
            try:
                link = link_ptn.findall(item)[0]
                title = title_ptn.findall(item)[0]
                isbn = isbn_ptn.findall(item)[0].replace('-', '')
                record = record_ptn.findall(link)[0]
            except:
                logging.warning('link %s, title %s isbn %s, record %s' % (link, title, isbn, record))
                failed_count = failed_count + 1
                parse_count = parse_count + 1
                continue

            ## If the link is last parst url, then break, or update last link
            if link == library_result.last_link:
                logging.info('last link == %s, break' % link)
                break
            else:
                if parse_count == 0:
                    ## Update the last_link in Library
                    library_result.last_link = link
                    library_result.put()
                    logging.info('Revise last link to %s' % link)

            ## Link to book link to parse more data
            book_page_source = urllib2.urlopen(link).read().decode('utf-8')
            try:
                find_number = find_number_ptn.findall(book_page_source)[0]
                status = status_ptn.findall(book_page_source)[0]
            except:
                logging.warning('find_number is empty in %s' % link)
                failed_count = failed_count + 1
                parse_count = parse_count + 1
                continue

            ## Search if the record in db, then skip this record
            book_result = Books.query(Books.link == link).get()
            if book_result == None:
                Books(school=library_result.school_name, title=title, link=link,
                      isbn=isbn, find_number=find_number, record=record, status=status).put()
                      
                logging.info('store %s into db' % link)
                success_count = success_count + 1
                parse_count = parse_count + 1
            else:
                logging.info('link %s already in db' % link)
                parse_count = parse_count + 1

        logging.info('Success count %s, failed count %s.' % (success_count, failed_count))
