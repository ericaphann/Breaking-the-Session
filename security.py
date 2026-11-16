import hashlib
import hmac


def user_agent_hash(user_agent):
    """Turn the browser's User-Agent text into a fingerprint (SHA-256)."""
    return hashlib.sha256((user_agent or "").encode()).hexdigest()


def binding_matches(stored_hash, user_agent):
    """Does this request's browser match the one that logged in?"""
    if stored_hash is None:
        return False
    return hmac.compare_digest(stored_hash, user_agent_hash(user_agent))