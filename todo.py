import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_talisman import Talisman

from app import create_app, db

app = create_app()
csp = {
    'default-src': [
        "'self'"
    ],
    'script-src': [
        "'self'",
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js'
    ],
    'style-src': [
        "'self'",
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'
    ],
    'img-src': [
        "'self'",
        'data:'
    ],
    'font-src': [
        "'self'",
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'
    ],
    'frame-ancestors': [
        "'self'"
    ],
    'form-action': [
        "'self'"
    ],
}

Talisman(app, content_security_policy=csp)
