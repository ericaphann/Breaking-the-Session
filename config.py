
import os

# Security mode:
# 0 = Vulnerable
# 1 = Hardened cookies, no regeneration
# 2 = Session regeneration
# 3 = Regeneration + hardened cookies + binding

SECURITY_MODE = int(os.environ.get("SECURITY_MODE", "0"))

if SECURITY_MODE not in (0, 1, 2, 3):
    raise ValueError("SECURITY_MODE must be 0, 1, 2, or 3")

# Only allow the intentionally vulnerable demo on localhost.
DEMO_HOST = "127.0.0.1"
DEMO_PORT = 5000

COOKIE_NAME = "demo_session"

SESSION_LIFETIME_SECONDS = 1800

# Cookie hardening is enabled in Modes 1 and 3.
HARDEN_COOKIES = SECURITY_MODE in (1, 3)

# Regeneration and binding will be implemented by Krupali.
REGENERATE_ON_LOGIN = SECURITY_MODE in (2, 3)
BIND_USER_AGENT = SECURITY_MODE == 3

# Explicitly enable the URL planting demonstration
# in the controlled local lab.
ALLOW_URL_SESSION_PLANTING = True
