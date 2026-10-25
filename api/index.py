import sys
import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app


class VercelPathMiddleware:
    """
    WSGI middleware for Vercel Serverless deployments.
    When vercel.json rewrites /(.*) -> /api/index, Vercel sets
    HTTP_X_MATCHED_PATH (or x-matched-path) to the original URL requested
    by the client (e.g. /dashboard, /personal-credit, /api/login, /).
    This middleware restores PATH_INFO so Flask's URL router matches
    the original intended route.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # Diagnostic dump endpoint
        if "dump_env=1" in environ.get("QUERY_STRING", ""):
            import json
            data = {k: str(v) for k, v in environ.items() if isinstance(v, (str, int, bool))}
            body = json.dumps(data, indent=2).encode("utf-8")
            start_response("200 OK", [("Content-Type", "application/json")])
            return [body]

        matched = environ.get("HTTP_X_MATCHED_PATH") or environ.get("x-matched-path")
        if matched:
            if "?" in matched:
                matched = matched.split("?")[0]
            if matched not in ("/api/index", "/api/index.py", "/api"):
                environ["PATH_INFO"] = matched
        elif environ.get("PATH_INFO") in ("/api/index", "/api/index.py", "/api"):
            # If no matched header and PATH_INFO is the entrypoint, default to root "/"
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


# Apply middleware to Flask WSGI layer
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Expose standard WSGI entrypoint names for Vercel
handler = app
application = app
