
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import (
    SECURITY_MODE,
    DEMO_HOST,
    DEMO_PORT,
    COOKIE_NAME,
    HARDEN_COOKIES,
    ALLOW_URL_SESSION_PLANTING
)

from sessions import (
    create_session,
    get_session,
    authenticate_session,
    invalidate_session
)


app = Flask(__name__, template_folder="Website")

# Local educational demonstration account.
# Password is hashed rather than stored as plaintext.
DEMO_USERS = {
    "student": generate_password_hash("DemoPass123!")
}


def set_session_cookie(response, session_id):
    """Set the browser's session cookie."""
    response.set_cookie(
        COOKIE_NAME,
        session_id,
        httponly=HARDEN_COOKIES,
        secure=HARDEN_COOKIES,
        samesite="Lax" if HARDEN_COOKIES else None,
        path="/"
    )
    return response


def get_or_create_session():
    """
    Find an existing session or create a new one.

    The URL parameter is deliberately accepted in this
    local educational lab to simulate session planting.
    """
    planted_id = request.args.get("sid")

    if ALLOW_URL_SESSION_PLANTING and planted_id:
        planted_session = get_session(planted_id)

        if planted_session is not None:
            return planted_id

    cookie_id = request.cookies.get(COOKIE_NAME)

    if get_session(cookie_id) is not None:
        return cookie_id

    return create_session()


@app.route("/")
def home():
    session_id = get_or_create_session()
    response = make_response(
        render_template(
            "index.html",
            mode=SECURITY_MODE
        )
    )

    return set_session_cookie(response, session_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    session_id = get_or_create_session()

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        password_hash = DEMO_USERS.get(username)

        if (
            password_hash is None
            or not check_password_hash(password_hash, password)
        ):
            response = make_response(
                render_template(
                    "login.html",
                    error="Invalid username or password"
                ),
                401
            )
            return set_session_cookie(response, session_id)

        if SECURITY_MODE in (2, 3):
            return (
                "Secure modes are not implemented yet. "
                "Krupali will add session regeneration.",
                501
            )

        # Intentionally vulnerable Modes 0 and 1:
        # Authenticate without regenerating the ID.
        authenticate_session(session_id, username)

        response = make_response(
            redirect(url_for("dashboard"))
        )

        return set_session_cookie(response, session_id)

    response = make_response(
        render_template("login.html", error=None)
    )

    return set_session_cookie(response, session_id)


@app.route("/dashboard")
def dashboard():
    session_id = request.cookies.get(COOKIE_NAME)
    session = get_session(session_id)

    if session is None or not session["authenticated"]:
        return "401 Unauthorized: Please log in.", 401

    return render_template(
        "dashboard.html",
        username=session["username"],
        mode=SECURITY_MODE
    )


@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.cookies.get(COOKIE_NAME)
    invalidate_session(session_id)

    response = make_response(
        redirect(url_for("home"))
    )

    response.delete_cookie(
        COOKIE_NAME,
        path="/"
    )

    return response


if __name__ == "__main__":
    app.run(
        host=DEMO_HOST,
        port=DEMO_PORT,
        debug=False
    )
