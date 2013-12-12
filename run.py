import os
import sys

# App Engine projects must include the source of thirdparty libraries
# such as Google's apiclient. These are stored in a lib folder so as not
# to clutter the application code. Here, a sys.path maninipulation is
# performed to ensure those modules found in lib are available to the
# application at runtime.
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))
from application.main import application