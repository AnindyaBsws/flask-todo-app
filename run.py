from app import create_app,db
import secrets
from flask import Flask, session, request, redirect, url_for, flash
import os

app = create_app()

if os.environ.get("FLASK_ENV") == "development":
    with app.app_context():
        db.create_all()


app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

@app.before_request
def set_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))