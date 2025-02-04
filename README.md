# School Security System

A Flask-based web application for school security that allows parents to upload their photos for identification.

## Features
- Unique link generation for parents
- Photo upload and storage
- PostgreSQL database integration
- Docker containerization

## Purpose
The goal of this project is to enhance school security by providing a reliable way to identify parents when picking up their children.

## Technology Stack
- **Flask**: A lightweight framework ideal for creating REST APIs
- **PostgreSQL**: A reliable relational database for storing data
- **Docker**: Ensures a uniform development environment and simplifies deployment
- **SQLAlchemy**: An ORM for convenient database interaction
- **Alembic**: A migration system for managing the database schema

## Requirements
- Docker
- Docker Compose

## Quick Start
1. Clone the repository:
```bash
git clone <repository-url>
cd task1FOQUS
```

2. Create .env file:
```bash
cp .env.example .env
```

3. Run with Docker:
```bash
docker-compose up -d
```

4. Access the application:
```
http://localhost:5001
```

## API Endpoints
- `POST /generate_link`: Generate unique link for parent
- `GET/POST /onboarding/<unique_id>`: Photo upload page
- `GET /`: Admin dashboard

## Project Structure
```
task1FOQUS/
├── app.py              # Main application
├── models.py           # Database models
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── migrations/        # Database migrations
├── templates/         # HTML templates
└── uploads/           # Photo upload directory
```

## Troubleshooting

### Common Issues
1. **Database Unavailable**
   - Check container status: `docker-compose ps`
   - Check logs: `docker-compose logs db`
   
2. **Photo Upload Errors**
   - Check upload directory permissions
   - Check web server logs: `docker-compose logs web`

3. **Migration Issues**
   - Check database connection
   - Run migrations manually: `docker-compose exec web alembic upgrade head`

## Examples

### Creating a Parent Record
```python
parent = Parent(
    unique_id=str(uuid.uuid4()),
    parent_name="John",
    parent_surname="Doe",
    child_name="Jane"
)
db_session.add(parent)
db_session.commit()
```

### Uploading a Photo
```python
photo = Photo(
    parent_id=parent.id,
    filename=f"{unique_id}_{timestamp}.jpg"
)
db_session.add(photo)
db_session.commit()
```

## References
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
