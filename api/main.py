from firebase_functions import https_fn
from index import app

# Expose the Flask app as a Cloud Function
@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
