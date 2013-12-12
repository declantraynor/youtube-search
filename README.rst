What is it?
-----------

YouTube Search is a small web application written in Python. It was built using the 
`webapp 2 <http://webapp-improved.appspot.com/>`_ framework for `Google AppEngine <https://developers.google.com/appengine/>`_. 
The app allows users to perform keyword-based searches for YouTube videos by using 
the `YouTube Data API <https://developers.google.com/youtube/v3/>`_.


Other Frameworks / Libraries Used
---------------------------------

- `Jinja2 <http://jinja.pocoo.org/>`_ for templating.
- `Bootstrap <http://getbootstrap.com>`_ for rapid frontend development.


Demo
----

You can play with the application at `http://coderdex-youtube-search.appspot.com <http://coderdex-youtube-search.appspot.com>`_.


Running Locally
---------------

You can run the application using the development server that comes with the `AppEngine SDK <https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python>`_:

.. code-block:: bash

    $ git clone https://github.com/declantraynor/youtube-search
    $ dev_appserver.py youtube-search
    
The YouTube Data API requires all requests to be authenticated, so you need to set a valid API key in app.yaml:

.. code-block:: yaml

    env_variables:
      YOUTUBE_API_KEY = 'MyReallySuperSecretAPIKey'
