import os

import webapp2

from handlers import IndexHandler, SearchHandler


routes = [
    ('/', IndexHandler),
    ('/search', SearchHandler)
]

application = webapp2.WSGIApplication(routes)