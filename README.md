# Breaking-the-Session
Group Final Project for ITIS 6200 Group 6

A small web application in Flask (Python) with a standard username/password login flow. The app issues a session cookie on first visit, authenticates users through a login form, and grants access to a protected page after login. Flask’s default session is a client-side signed cookie, which has no server-side session ID to fixate, so we will implement our own server-side session store (an in-memory dictionary keyed by session ID) and set the session cookie ourselves. This mirrors a common real-world pattern in which a session ID issued before authentication keeps being used after login.

Windows:
Create the environment: python -m venv venv
Install all dependencies with: pip install -r requirements.txt
Select Security Mode using the variables below:
$env:SECURITY_MODE="0"
$env:SECURITY_MODE="1"
$env:SECURITY_MODE="2"
$env:SECURITY_MODE="3"
Run the application: python app.py

Mac test: 
source .venv/bin/activate
python -m pip install -r requirements.txt
SECURITY_MODE=0 python app.py
SECURITY_MODE=1 python app.py
SECURITY_MODE=2 python app.py
SECURITY_MODE=3 python app.py


Login:
Username: student
Password: DemoPass123!

