
import secrets
import time

from config import SESSION_LIFETIME_SECONDS


# In-memory server-side session store
sessions = {}


def generate_session_id():
    """Generate a cryptographically secure session ID."""
    return secrets.token_urlsafe(32)


def create_session():
    """Create a new anonymous session."""
    session_id = generate_session_id()

    sessions[session_id] = {
        "username": None,
        "authenticated": False,
        "created_at": time.time()
    }

    return session_id


def get_session(session_id):
    """Look up a session and reject expired sessions."""
    if not session_id:
        return None

    session = sessions.get(session_id)

    if session is None:
        return None

    age = time.time() - session["created_at"]

    if age > SESSION_LIFETIME_SECONDS:
        sessions.pop(session_id, None)
        return None

    return session


def authenticate_session(session_id, username):
    """
    Vulnerable authentication behavior:
    Mark the existing session as authenticated
    without changing its session ID.
    """
    session = get_session(session_id)

    if session is None:
        return False

    session["username"] = username
    session["authenticated"] = True

    return True


def invalidate_session(session_id):
    """Delete a session from the server-side store."""
    if session_id:
        sessions.pop(session_id, None)


def reset_sessions():
    """Clear the session store between demonstrations."""
    sessions.clear()
