# Event Management API

REST API for managing events and user registrations, built with Django and Django REST Framework.

The project demonstrates feature-based architecture with separation between API and domain layers, Dockerized setup, JWT authentication, and real email notifications.

---

## 🚀 Features

- User registration and authentication using JWT
- Event CRUD (create, read, update, delete)
- Public event listing
- User registration for events
- Organizer-only access to event registrations
- Filtering, search and ordering
- Email notification on successful registration
- Django admin panel
- Dockerized setup with PostgreSQL

---

## ▶️ How to run and test the project

### Run with Docker (recommended)

1. Build and start containers

docker compose up --build

This will start:
- Django application (Gunicorn)
- PostgreSQL database

2. Apply database migrations

docker compose exec web python manage.py migrate

3. Create admin user

docker compose exec web python manage.py createsuperuser

4. Access the application

API documentation:
http://127.0.0.1:8000/api/docs/

Django admin panel:
http://127.0.0.1:8000/admin/

---

### Quick API check

1. Register a user  
POST /api/auth/register/

2. Login and obtain JWT token  
POST /api/auth/login/
[
3. Click Authorize in Swagger and paste access token

4. Create an event  
POST /api/events/

5. Register another user for the event  
POST /api/events/{id}/register/

6. Check registrations (organizer only)  
GET /api/events/{id}/registrations/

---

## 🧱 Project Architecture

The project uses a feature-based architecture inside Django apps.

API layer and domain logic are clearly separated.

Architecture principles:

- API layer contains only HTTP-related logic
- Domain layer contains business logic and database access
- Views are thin and delegate logic to services
- Side effects (email notifications) are isolated from core business logic
- Database access is centralized in selectors

---

## 🔐 Authentication

Authentication is implemented using JWT.

Available endpoints:

- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/refresh/

---

## 📅 Events API

Available endpoints:

- GET /api/events/
- POST /api/events/
- GET /api/events/{id}/
- PATCH /api/events/{id}/
- DELETE /api/events/{id}/
- POST /api/events/{id}/register/
- GET /api/events/{id}/registrations/

Permissions:

- Events are public for reading
- Only the organizer can update or delete an event
- Only the organizer can view registrations list

---

## 🔍 Filtering, Search and Ordering

Supported query parameters:

- search — search by title or description
- location — filter by location
- starts_at__gte — events starting after date
- starts_at__lte — events starting before date
- organizer — filter by organizer id
- ordering — ordering by fields (e.g. starts_at, created_at)

Example request:

/api/events/?search=django&location=kyiv&ordering=-starts_at

---

## 📧 Email Notifications

After successful registration for an event, the user receives an email notification.

- Email sending is implemented via Django email backend
- SMTP credentials are provided via environment variables
- Email delivery is isolated from business logic

---

## 🐳 Environment Variables

Example .env file:

DJANGO_SETTINGS_MODULE=config.settings.local  
DJANGO_SECRET_KEY=your-secret-key  
DJANGO_DEBUG=1  

POSTGRES_DB=event_manager  
POSTGRES_USER=event_manager  
POSTGRES_PASSWORD=event_manager  
POSTGRES_HOST=db  
POSTGRES_PORT=5432  

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  
EMAIL_HOST=smtp.gmail.com  
EMAIL_PORT=587  
EMAIL_USE_TLS=1  
EMAIL_HOST_USER=your_email@gmail.com  
EMAIL_HOST_PASSWORD=your_app_password  
DEFAULT_FROM_EMAIL=Event Manager <your_email@gmail.com>

---

## 🗄 Database Indexes

Indexes are added for frequently queried fields.

Events:
- organizer
- starts_at
- location

Event registrations:
- event
- user
- created_at
- unique constraint on (event, user)
