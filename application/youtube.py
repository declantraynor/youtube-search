import os

import apiclient.discovery
from apiclient.errors import HttpError


YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube_api_client = apiclient.discovery.build(YOUTUBE_API_SERVICE_NAME,
                                               YOUTUBE_API_VERSION,
                                               developerKey=YOUTUBE_API_KEY)


def search_videos(options):
    '''Perform a keyword search for videos via the YouTube Data API.

    Positional arguments:
    options -- a dictionary of optional parameters to be submitted in
    the YouTube API request.

    Returns:
    A tuple of video results (list) and search metatdata (dict)

    '''
    request_params = {
        'q': options.get('q', ''),
        'part': 'id, snippet',
        'type': 'video',
        'maxResults': options.get('max_results', 30),
        'pageToken': options.get('page_token', '')
    }

    response = youtube_api_client.search().list(**request_params).execute()

    search_metadata = {}
    results = []

    # Parse the api response headers for important metadata about the
    # search performed
    page_info = response.get('pageInfo', {})

    search_metadata['total_results'] = page_info.get('totalResults', 0)
    search_metadata['results_per_page'] = page_info.get('resultsPerPage', 0)
    search_metadata['next_page_token'] = response.get('nextPageToken', 0)
    search_metadata['prev_page_token'] = response.get('prevPageToken', 0)

    # Parse the 'items' array of the api response to build small video
    # dictionaries containing just those fields we are interested in
    for video in response.get('items', []):
        results.append({
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'thumbnail': video['snippet']['thumbnails']['medium']['url'],
            'url': 'http://youtube.com/watch?v=%s' % video['id']['videoId']
        })

    return (results, search_metadata)