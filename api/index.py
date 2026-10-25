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
    Extracts the original requested route:
    1. From `__path__` query parameter forwarded by vercel.json rewrite: /api/index.py?__path__=$1
    2. Fallback to HTTP_X_MATCHED_PATH / HTTP_X_VERCEL_PATH headers if present.
    Ensures all Flask routes (e.g. /dashboard, /personal-credit, /settings, /api/login)
    are routed accurately.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path_override = None
        query_string = environ.get("QUERY_STRING", "")

        # 1. Check for `__path__` in QUERY_STRING forwarded by vercel.json rewrite
        if "__path__=" in query_string:
            parsed = urllib.parse.parse_qs(query_string, keep_blank_values=True)
            if "__path__" in parsed:
                raw_path = parsed.pop("__path__")[0]
                if raw_path:
                    path_override = "/" + raw_path.lstrip("/")
                else:
                    path_override = "/"
                # Reconstruct QUERY_STRING without `__path__`
                environ["QUERY_STRING"] = urllib.parse.urlencode(parsed, doseq=True)

        # 2. Fallback to Vercel headers if __path__ was not found or empty
        if not path_override:
            for header in [
                "HTTP_X_MATCHED_PATH",
                "HTTP_X_VERCEL_PATH",
                "HTTP_X_FORWARDED_URI",
                "x-matched-path",
                "REQUEST_URI",
            ]:
                val = environ.get(header)
                if val and val not in ("/api/index.py", "/api/index", "/(.*)"):
                    if "?" in val:
                        val = val.split("?")[0]
                    path_override = "/" + val.lstrip("/")
                    break

        # 3. If path_override is determined, update PATH_INFO
        if path_override:
            environ["PATH_INFO"] = path_override

        return self.wsgi_app(environ, start_response)


# Apply middleware to Flask WSGI layer
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Expose standard WSGI entrypoint names for Vercel
handler = app
application = app
