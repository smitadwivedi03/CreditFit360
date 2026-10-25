import sys
import os
import urllib.parse

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app


class VercelPathMiddleware:
    """
    WSGI middleware for Vercel Serverless deployments.
    Extracts the original requested route from the `__path__` parameter
    passed by vercel.json rewrite: /api/index?__path__=$1
    Restores PATH_INFO and cleans QUERY_STRING so all Flask routes
    (e.g. /dashboard, /personal-credit, /settings, /api/login) match properly.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        query_string = environ.get("QUERY_STRING", "")

        if "__path__=" in query_string:
            parsed = urllib.parse.parse_qs(query_string, keep_blank_values=True)
            if "__path__" in parsed:
                raw_path = parsed.pop("__path__")[0]
                if raw_path:
                    environ["PATH_INFO"] = "/" + raw_path.lstrip("/")
                else:
                    environ["PATH_INFO"] = "/"
                environ["QUERY_STRING"] = urllib.parse.urlencode(parsed, doseq=True)
        elif environ.get("PATH_INFO") in ("/api/index", "/api/index.py", "/api"):
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


# Apply middleware to Flask WSGI layer
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Expose standard WSGI entrypoint names for Vercel
handler = app
application = app
