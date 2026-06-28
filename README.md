# Travel-Planner
# Travel Planner API

A REST API for managing travel projects and places, built with Django and Django REST Framework.

## Tech Stack
- Python / Django
- Django REST Framework
- SQLite
- Art Institute of Chicago API

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   python -m venv venv
   venv\Scripts\activate
3. Install dependencies:
   pip install django djangorestframework requests
4. Run migrations:
   python manage.py migrate
5. Start the server:
   python manage.py runserver

## API Endpoints

### Projects
- GET /api/projects/ — list all projects
- POST /api/projects/ — create a project
- GET /api/projects/{id}/ — get a project
- PUT /api/projects/{id}/ — update a project
- DELETE /api/projects/{id}/ — delete a project

### Places
- GET /api/projects/{id}/places/ — list all places
- POST /api/projects/{id}/places/ — add a place
- GET /api/projects/{id}/places/{place_id}/ — get a place
- PUT /api/projects/{id}/places/{place_id}/ — update a place (notes/visited)

## Business Rules
- A project can have 1-10 places
- A project cannot be deleted if any place is marked as visited
- Places are validated against the Art Institute of Chicago API
- A place cannot be added to the same project twice
- A project is marked as completed when all places are visited
