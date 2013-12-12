import os

import jinja2


TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIRECTORY),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_template(template_name, template_data={}):
    '''Conveniently generate markup for a given template and dataset.

    Allows calling code (e.g. in request handlers) to remain unaware of
    the underlying Jinja2 environment setup.

    Positional arguments:
    template_name -- the file name of the HTML template to be rendered

    Keyword arguments:
    template_data -- a dictionary of data to be interpolated with named
        placeholders found in the provided template (default={})

    Returns:
    A string containing markup rendered from the template

    '''
    template = JINJA_ENVIRONMENT.get_template(template_name)
    return template.render(template_data)