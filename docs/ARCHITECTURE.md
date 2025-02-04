# System Architecture Documentation

## Overview
The Parent Onboarding Service is a Flask-based web application designed for secure parent identification in schools. It follows a microservices architecture pattern and is deployed on AWS EC2.

## System Components

### 1. Web Application (Flask)
- Handles HTTP requests
- Manages user sessions
- Processes form submissions
- Serves HTML templates
- Validates uploaded photos

### 2. Database (PostgreSQL)
- Stores parent information
- Manages photo metadata
- Handles relationships between entities
- Ensures data integrity

### 3. File Storage
- Manages uploaded photos
- Implements secure file handling
- Provides backup mechanisms

### 4. AWS Integration
- EC2 for application hosting
- CloudWatch for monitoring
- S3 for photo backups
- IAM for security

## Data Model

### Parent Entity
```python
class Parent:
    id: Integer (Primary Key)
    unique_id: String (UUID)
    parent_name: String
    parent_surname: String
    child_name: String
    created_at: DateTime
    photos: Relationship[Photo]
```

### Photo Entity
```python
class Photo:
    id: Integer (Primary Key)
    parent_id: Integer (Foreign Key)
    filename: String
    uploaded_at: DateTime
    parent: Relationship[Parent]
```

## Security Architecture

### Authentication & Authorization
- Unique link generation for each parent
- UUID-based access control
- Session management

### Data Protection
- HTTPS encryption
- Secure file uploads
- Database encryption
- AWS security groups

### Monitoring & Logging
- CloudWatch integration
- Error tracking
- Access logging
- Performance metrics

## System Interactions

### Photo Upload Flow
1. Parent receives unique link
2. Accesses onboarding page
3. Uploads photo
4. System validates photo
5. Photo stored securely
6. Metadata saved to database

### Admin Dashboard Flow
1. Admin accesses dashboard
2. System retrieves parent list
3. Displays parent information
4. Shows photo status

## Performance Considerations

### Optimization Techniques
- Image compression
- Database indexing
- Caching strategies
- Load balancing ready

### Scalability
- Horizontal scaling support
- Database connection pooling
- Stateless application design
- AWS auto-scaling ready

## Deployment Architecture

### Production Environment
```
[Client] -> [Nginx] -> [Flask App] -> [PostgreSQL]
                    -> [File Storage]
                    -> [CloudWatch]
```

### Development Environment
```
[Docker Compose]
  |- Web Service
  |- PostgreSQL
  |- Volumes
```

## Error Handling

### Application Errors
- Input validation
- File processing errors
- Database errors
- Network timeouts

### System Errors
- Service unavailability
- Database connection issues
- Storage capacity issues
- AWS service errors

## Maintenance Procedures

### Backup Strategy
- Daily database backups
- Photo backups to S3
- Configuration backups
- Automated scheduling

### Update Procedures
- Zero-downtime updates
- Database migrations
- Configuration updates
- Security patches

## Development Guidelines

### Code Structure
```
/app
  ├── app.py           # Main application
  ├── models.py        # Database models
  ├── config.py        # Configuration
  ├── requirements.txt # Dependencies
  ├── templates/       # HTML templates
  ├── static/          # Static files
  ├── migrations/      # Database migrations
  └── uploads/         # Photo storage
```

### Best Practices
- PEP 8 compliance
- Type hinting
- Comprehensive testing
- Documentation
- Code review process

## Future Improvements

### Planned Features
- Multi-language support
- Face recognition
- Bulk photo upload
- API authentication
- Mobile app support

### Technical Debt
- Migration to S3
- API versioning
- Test coverage
- Performance optimization
