from app import create_app,db
import secrets
from flask import Flask, session, request, redirect, url_for, flash

app = create_app()

with app.app_context():
    db.create_all()


app.secret_key = 'your-very-secure-secret-key'

@app.before_request
def set_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

if __name__ == "__main__":
    app.run(debug=True)