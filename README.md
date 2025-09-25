# Bookshelf Backend API

Flask REST API for managing books, authors, reviews, and user collections.

## Tech Stack
- Flask + Flask-RESTful
- SQLite + SQLAlchemy
- Python 3.12

## Models
- **User**: username, email, password, role
- **Author**: name, bio, birth_year
- **Book**: title, description, isbn, publication_year
- **Category**: name, description, background_image
- **Review**: rating (1-5), content
- **UserBookCollection**: status, date_added

## API Endpoints
- `/users` - User CRUD
- `/authors` - Author CRUD
- `/books` - Book CRUD (filter by `?admin_id=<id>`)
- `/categories` - Category CRUD
- `/reviews` - Review CRUD
- `/collections` - User collection CRUD

## Setup
```bash
pipenv install
pipenv shell
python seed.py
python app.py
```

API runs on `http://localhost:5000`

## License
This project is licensed under the MIT License 

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Collaboration
This project was created under the collaboration of Muzna and Derrick . We are open to having more collaborators and contributions 

## Author
Username : Muzna Ebrahim 
Email : ebrahimmuznah98@gmail.com 

Username : Derrickgabe 
Email : derrickg844@gmail.com
