import logging
import random
import urllib

import webapp2

from models import search_group_key, Search
from utils import render_template
from youtube import HttpError, search_videos


def build_url(url_base, params):
    '''Build URL with an escaped query string.'''
    return '%s?%s' % (url_base, urllib.urlencode(params))


def get_previous_searches():
    '''Build a list of tuples (url, keywords) describing 30 most
    recent searches stored by the application.'''
    previous_searches = []

    for search in Search.query_by_most_recent().fetch(30):
        previous_searches.append((search.url, search.keywords))

    return previous_searches


def get_random_search_suggestion():
    return random.choice([
        'KITTENS',
        'gangnam style',
        'how to wrap a cat for christmas',
        'harlem shake',
        'smooth mcgroove',
        'drat the luck'
    ])


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        error = self.request.get('error', '')

        template_data = {
            'previous_searches': get_previous_searches(),
            'suggestion': get_random_search_suggestion()
        }

        if error and error == 'empty_query':
            template_data['error'] = {
                'exclamation': 'You don\'t search so good, buddy.',
                'description': 'But that\'s okay. Try typing some keywords this time.'
            }
        elif error and error == 'api_error':
            template_data['error'] = {
                'exclamation': 'Well, this is embarrassing.',
                'description': 'There was a problem running your search. Please try again later.'
            }

        self.response.write(render_template('index.html', template_data))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('q', '')
        page_token = self.request.get('page', '')

        # Perform the video search
        try:
            results, search_metadata = search_videos({
                'q': urllib.unquote(query),
                'page_token': page_token
            })
        except HttpError as error:
            if error.resp.status is 403:
                # Application not authenticated with YouTube API
                logging.error('Please ensure a valid YouTube API key is \
                    set in app.yaml')
            return self.redirect(build_url('/', [
                ('error', 'api_error')
            ]))

        # Pack the results and other data required by the template and
        # render
        template_data = {
            'query': urllib.unquote(query),
            'total_results': search_metadata['total_results'],
            'results': results,
            'results_per_page': search_metadata['results_per_page'],
            'previous_searches': get_previous_searches(),
            'suggestion': get_random_search_suggestion()
        }

        if search_metadata['next_page_token']:
            template_data['next_page_url'] = build_url('/search', [
                ('q', query),
                ('page', search_metadata['next_page_token'])
            ])

        if search_metadata['prev_page_token']:
            template_data['prev_page_url'] = build_url('/search', [
                ('q', query),
                ('page', search_metadata['prev_page_token'])
            ])

        self.response.write(render_template('search.html', template_data))

    def post(self):
        query = self.request.get('q', '')
        page_token = self.request.get('page', '')

        # The user must enter a valid search query. If not, redirect to
        # index, providing an error which will determine the response
        # generated by IndexHandler
        if not query:
            return self.redirect(build_url('/', [
                ('error', 'empty_query')
            ]))

        # Save search query to the High Replication Datastore
        search = Search(parent=search_group_key())
        search.keywords = urllib.unquote(query)
        search.url = build_url('/search', [
            ('q', query)
        ])
        search.put()

        # Redirect to a URL that will trigger the YouTube API request
        # and render the response.
        return self.redirect(search.url)