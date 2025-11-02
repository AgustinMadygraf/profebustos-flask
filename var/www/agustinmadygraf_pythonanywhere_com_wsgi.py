# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = '/home/agustinmadygraf/profebustos-flask/src/infrastructure/flask'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application  # noqa



# ------------------------------------------------------------

# /var/www/<tu-app>.pythonanywhere.com_wsgi.py  (enlace desde el Web tab)
import sys

project_root = '/home/agustinmadygraf/profebustos-flask'
flask_dir    = project_root + '/src/infrastructure/flask'

for p in (flask_dir, project_root):
    if p not in sys.path:
        sys.path.insert(0, p)

from flask_app import app as application  # Flask app global -> WSGI "application"
