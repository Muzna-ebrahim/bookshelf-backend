#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run database migrations and seed data
python -c "
from server.config import app, db
from server.models import *
from server.seed import *

with app.app_context():
    db.create_all()
    seed_data()
"