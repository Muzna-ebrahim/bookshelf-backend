#!/usr/bin/env python3

import os
from server.config import app, db

# Import all models to ensure they're registered
from server.models import User, Author, Book, Review, UserBookCollection, Category

# Import routes
from server.app import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)