from django.db import models
from google.appengine.ext import ndb

class Library(ndb.Model):
    school_name = ndb.StringProperty()
    rss_url = ndb.StringProperty()
    last_link = ndb.StringProperty()

class Books(ndb.Model):
    school = ndb.StringProperty()
    title = ndb.StringProperty()
    link = ndb.StringProperty()
    isbn = ndb.StringProperty()
    find_number = ndb.StringProperty()
    record = ndb.StringProperty()
    status = ndb.StringProperty()

class UserTraceBooks(ndb.Model):
    isbn = ndb.StringProperty()
