#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, Author, Book, Review, UserBookCollection, Category

# Views go here!

def create_resource(model, name, required_fields, optional_fields=None):
    optional_fields = optional_fields or []
    
    class ResourceList(Resource):
        def get(self):
            return [item.to_dict() for item in model.query.all()], 200
        
        def post(self):
            data = request.get_json()
            try:
                kwargs = {field: data[field] for field in required_fields}
                kwargs.update({field: data.get(field) for field in optional_fields})
                item = model(**kwargs)
                db.session.add(item)
                db.session.commit()
                return item.to_dict(), 201
            except Exception as e:
                return {'error': str(e)}, 400
    
    class ResourceByID(Resource):
        def get(self, id):
            item = model.query.filter_by(id=id).first()
            return item.to_dict() if item else ({'error': f'{name} not found'}, 404)
        
        def patch(self, id):
            item = model.query.filter_by(id=id).first()
            if not item:
                return {'error': f'{name} not found'}, 404
            try:
                for attr, value in request.get_json().items():
                    setattr(item, attr, value)
                db.session.add(item)
                db.session.commit()
                return item.to_dict(), 200
            except Exception as e:
                return {'error': str(e)}, 400
        
        def delete(self, id):
            item = model.query.filter_by(id=id).first()
            if not item:
                return {'error': f'{name} not found'}, 404
            db.session.delete(item)
            db.session.commit()
            return {}, 204
    
    # Make class names unique
    ResourceList.__name__ = f'{name}List'
    ResourceByID.__name__ = f'{name}ByID'
    
    return ResourceList, ResourceByID

Users, UserByID = create_resource(User, 'User', ['username', 'email', 'password'], ['role'])
Authors, AuthorByID = create_resource(Author, 'Author', ['name'], ['bio', 'birth_year', 'user_id'])
Categories, CategoryByID = create_resource(Category, 'Category', ['name'], ['description', 'background_image'])
Reviews, ReviewByID = create_resource(Review, 'Review', ['rating', 'content', 'user_id', 'book_id'])
Collections, CollectionByID = create_resource(UserBookCollection, 'Collection', ['user_id', 'book_id', 'status'], ['date_added'])

class Books(Resource):
    def get(self):
        admin_id = request.args.get('admin_id')
        if admin_id:
            books = Book.query.filter_by(created_by=admin_id).all()
        else:
            books = Book.query.all()
        return [book.to_dict() for book in books], 200
    
    def post(self):
        data = request.get_json()
        try:
            book = Book(
                title=data['title'],
                author_id=data['author_id'],
                category_id=data['category_id'],
                created_by=data['created_by'],
                description=data.get('description'),
                isbn=data.get('isbn'),
                publication_year=data.get('publication_year')
            )
            db.session.add(book)
            db.session.commit()
            return book.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

class BookByID(Resource):
    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        return book.to_dict() if book else ({'error': 'Book not found'}, 404)
    
    def patch(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            return {'error': 'Book not found'}, 404
        try:
            for attr, value in request.get_json().items():
                setattr(book, attr, value)
            db.session.add(book)
            db.session.commit()
            return book.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
    
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            return {'error': 'Book not found'}, 404
        db.session.delete(book)
        db.session.commit()
        return {}, 204

# Add resources to API
api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')
api.add_resource(Authors, '/authors')
api.add_resource(AuthorByID, '/authors/<int:id>')
api.add_resource(Categories, '/categories')
api.add_resource(CategoryByID, '/categories/<int:id>')
api.add_resource(Books, '/books')
api.add_resource(BookByID, '/books/<int:id>')
api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewByID, '/reviews/<int:id>')
api.add_resource(Collections, '/collections')
api.add_resource(CollectionByID, '/collections/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)