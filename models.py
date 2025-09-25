from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

from config import db

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    background_image = db.Column(db.String(255))
    
    # One-to-many relationship
    books = db.relationship('Book', back_populates='category', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-books',)

# Many-to-many association table with user submittable attribute
class UserBookCollection(db.Model, SerializerMixin):
    __tablename__ = 'user_book_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # User submittable attribute
    
    # Relationships
    user = db.relationship('User', back_populates='book_collections')
    book = db.relationship('Book', back_populates='user_collections')
    
    # Serialization rules
    serialize_rules = ('-user.book_collections', '-user.reviews', '-user.authors', '-book.user_collections', '-book.reviews', '-book.author')

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='reader')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One-to-many relationships
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    authors = db.relationship('Author', back_populates='user', cascade='all, delete-orphan')
    
    # Many-to-many relationship
    book_collections = db.relationship('UserBookCollection', back_populates='user', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-reviews', '-authors', '-book_collections', '-password')

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    birth_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # One-to-many relationships
    user = db.relationship('User', back_populates='authors')
    books = db.relationship('Book', back_populates='author', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-user', '-books')

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    isbn = db.Column(db.String(13), unique=True)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # One-to-many relationships
    author = db.relationship('Author', back_populates='books')
    category = db.relationship('Category', back_populates='books')
    creator = db.relationship('User', foreign_keys=[created_by])
    reviews = db.relationship('Review', back_populates='book', cascade='all, delete-orphan')
    
    # Many-to-many relationship
    user_collections = db.relationship('UserBookCollection', back_populates='book', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-author', '-category', '-creator', '-reviews', '-user_collections')

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='reviews')
    book = db.relationship('Book', back_populates='reviews')
    

    
    # Validation
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    # Serialization rules
    serialize_rules = ('-user', '-book')