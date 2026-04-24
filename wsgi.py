from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response
from app import app

# Mount Flask app at /ailivechat
application = DispatcherMiddleware(
    Response("Not Found", status=404),
    {"/ailivechat": app}
)
