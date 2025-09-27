#!/usr/bin/env python3

import os
from server.config import app, db

# Import all models to ensure they're registered
from server.models import User, Author, Book, Review, UserBookCollection, Category

# Import routes - this registers all routes including the root route
import server.app

# Seed database with sample data
def seed_if_empty():
    with app.app_context():
        db.create_all()
        from server.models import User, Author, Book, Category
        
        # Only seed if database is empty
        if not User.query.first():
            # Create sample users
            admin = User(username="admin", email="admin@example.com", password="admin", role="admin")
            reader = User(username="reader", email="reader@example.com", password="reader", role="reader")
            derrick = User(username="derrick", email="derrickg844@gmail.com", password="password123", role="reader")
            db.session.add(admin)
            db.session.add(reader)
            db.session.add(derrick)
            db.session.commit()
            
            # Create categories
            fiction = Category(name="Fiction", description="Fiction books")
            science = Category(name="Science", description="Science books")
            mystery = Category(name="Mystery", description="Mystery books")
            db.session.add(fiction)
            db.session.add(science)
            db.session.add(mystery)
            db.session.commit()
            
            # Create authors
            author1 = Author(name="John Doe", bio="Sample author", user_id=admin.id)
            author2 = Author(name="Jane Smith", bio="Another author", user_id=admin.id)
            db.session.add(author1)
            db.session.add(author2)
            db.session.commit()
            
            # Create sample books
            book1 = Book(title="The Great Adventure", description="An amazing fictional story", author_id=author1.id, category_id=fiction.id, created_by=admin.id, isbn="1234567890", publication_year=2023)
            book2 = Book(title="Science Explained", description="Understanding the world through science", author_id=author2.id, category_id=science.id, created_by=admin.id, isbn="0987654321", publication_year=2024)
            db.session.add(book1)
            db.session.add(book2)
            db.session.commit()

seed_if_empty()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)