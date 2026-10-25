import sys
import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app


class VercelPathMiddleware:
    """
    WSGI middleware for Vercel Serverless deployments.
    Extracts the original requested route from Vercel's HTTP_X_MATCHED_PATH header
    so Flask routes (e.g. /dashboard, /personal-credit, /settings, /api/login)
    match properly instead of collapsing to /api/index.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched = environ.get("HTTP_X_MATCHED_PATH") or environ.get("x-matched-path")
        if matched:
            if "?" in matched:
                matched = matched.split("?")[0]
            environ["PATH_INFO"] = matched
        return self.wsgi_app(environ, start_response)


# Apply middleware to Flask WSGI layer
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Expose standard WSGI entrypoint names for Vercel
handler = app
application = app
