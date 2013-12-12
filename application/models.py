from google.appengine.ext import ndb


def search_group_key(search_group_name='all_searches'):
    return ndb.Key('Search', search_group_name)


class Search(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    keywords = ndb.StringProperty(indexed=False)
    url = ndb.StringProperty(indexed=False)

    @classmethod
    def query_by_most_recent(cls, ancestor=search_group_key()):
        return cls.query(ancestor=ancestor).order(-cls.date)