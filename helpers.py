from flask import redirect, render_template, request, session
from functools import wraps


# login_required from CS50 finance
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message):
    """Renders message as an apology to user."""
    message = message
    return render_template("errormessage.html", message=message)
