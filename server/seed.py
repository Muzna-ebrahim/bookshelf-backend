#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Local imports
from app import app
from models import db, User, Author, Book, Review, UserBookCollection, Category

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        
        # Create tables
        db.create_all()
        
        # Clear existing data
        UserBookCollection.query.delete()
        Review.query.delete()
        Book.query.delete()
        Author.query.delete()
        Category.query.delete()
        User.query.delete()
        
        # Create users (admins)
        admin_data = [
            ('admin1', 'admin1@email.com', 'password123', 'admin'),
            ('admin2', 'admin2@email.com', 'password123', 'admin'),
            ('reader1', 'reader1@email.com', 'password123', 'reader')
        ]
        
        users = []
        for username, email, password, role in admin_data:
            user = User(username=username, email=email, password=password, role=role)
            users.append(user)
        
        db.session.add_all(users)
        db.session.commit()
        
        # Create categories
        category_data = [
            ('Philosophy', 'Books about philosophical thoughts and ideas', 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800'),
            ('Programming', 'Coding and software development books', 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800'),
            ('Science Fiction', 'Futuristic and imaginative stories', 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800'),
            ('History', 'Historical events and biographies', 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800')
        ]
        
        categories = []
        for name, desc, bg_img in category_data:
            category = Category(name=name, description=desc, background_image=bg_img)
            categories.append(category)
        
        db.session.add_all(categories)
        db.session.commit()
        
        # Create authors for each admin
        admin_users = [u for u in users if u.role == 'admin']
        authors = []
        
        for i, admin in enumerate(admin_users):
            if admin.username == 'admin1':
                author_names = ['Derrick', f'Author {i+1}B']
            else:
                author_names = [f'Author {i+1}A', f'Author {i+1}B']
            for name in author_names:
                author = Author(
                    name=name,
                    bio=f'Author managed by {admin.username}',
                    birth_year=randint(1970, 2000),
                    user_id=admin.id
                )
                authors.append(author)
        
        db.session.add_all(authors)
        db.session.commit()
        
        # Create books for each admin
        books = []
        book_templates = [
            ('Philosophy of Mind', 'Exploring consciousness and thought'),
            ('Python Mastery', 'Advanced programming techniques'),
            ('Space Odyssey', 'Journey through the cosmos'),
            ('Ancient Civilizations', 'Lost worlds and forgotten empires')
        ]
        
        for i, admin in enumerate(admin_users):
            admin_authors = [a for a in authors if a.user_id == admin.id]
            for j, (title, desc) in enumerate(book_templates):
                book = Book(
                    title=f"{title} - Admin {i+1}",
                    description=desc,
                    isbn=f"978-{randint(1000000000, 9999999999)}",
                    publication_year=randint(2020, 2024),
                    author_id=rc(admin_authors).id,
                    category_id=categories[j % len(categories)].id,
                    created_by=admin.id
                )
                books.append(book)
        
        db.session.add_all(books)
        db.session.commit()
        
        # Create reviews
        reviews = []
        
        db.session.add_all(reviews)
        db.session.commit()
        
        # Create user book collections
        collections = []
        
        db.session.add_all(collections)
        db.session.commit()
        
        print("Seed completed!")
        print(f"Created {len(users)} users")
        print(f"Created {len(authors)} authors")
        print(f"Created {len(books)} books")
        print(f"Created {len(reviews)} reviews")
        print(f"Created {len(collections)} collections")