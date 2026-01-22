# AGENTS.md

This file contains guidelines and commands for agentic coding assistants working in this Django REST API project.

## Project Overview

**Project**: Echoo - Real-time chat application backend  
**Stack**: Django 5.2 + Django REST Framework + Djoser + SQLite  
**Tailwind CSS: Styles of the UIs**
**Package Manager**: UV (modern Python package manager)  
**Python**: 3.14+

## Essential Commands

### Package Management
```bash
uv sync                   # Install dependencies
uv add <package>          # Add new dependency
uv run <command>          # Run commands in virtual environment
```

### Django Management
This project uses `uv` for dependency management. **Never use bare `python` or `pip` commands.** Always prefix Python commands with `uv run`:

```bash
# Incorrect
python manage.py runserver

# Correct
uv run python manage.py runserver          # Start dev server (default: 127.0.0.1:8000)
uv run python manage.py test               # Run all tests
uv run python manage.py test <app>         # Run tests for specific app
uv run python manage.py test <app>.<Test>  # Run single test class
uv run python manage.py test <app>.<Test>.<method>  # Run single test method
uv run python manage.py makemigrations     # Create migrations
uv run python manage.py migrate            # Apply migrations
uv run python manage.py check              # Check project configuration
uv run python manage.py shell              # Django shell
uv run python manage.py createsuperuser    # Create admin user
uv run python manage.py drf_create_token   # Create auth token
```

### Environment Setup
- Copy `.env.example` to `.env` (if exists)
- Set `SECRET_KEY` and `DEBUG` in `.env`
- Use `uv sync` to install dependencies

## Code Style Guidelines

- Follow PEP 8, unless specified differently in this file.
- ALWAYS provide type hints for every function that is not a view (especially in utils.py files)
- Each app should have its own `base.html` template
- Avoid using helper functions and complex structures when something can easily be solved with a single function
- create each Python file that is not a default file coming with a new django installation, with this header:

```py
"""
Script Name : <name_of_python_script>
Description : Describe the module or function here
Author      : @tonybnya
"""
```

### Django/Python Conventions

**Imports**:
- Standard library imports first
- Third-party imports second  
- Django imports third
- Local imports last
- Use absolute imports for Django apps: `from chat.models import Message`

**Models**:
- Use `BigAutoField` for primary keys (project default)
- Include `created_at` and `updated_at` timestamps where appropriate
- Use descriptive field names and help_text
- Add `__str__` methods for all models
- Use proper Django field types (CharField, TextField, etc.)

**Views/Serializers**:
- Use Django REST Framework class-based views
- Create separate serializers for each model
- Use `ModelSerializer` when possible
- Implement proper validation in serializers
- Return appropriate HTTP status codes

**URLs**:
- Use path() instead of url() for Django 2.0+
- Include app-level URLs in project URLs
- Use descriptive URL names with app prefix: `chat:message-list`

**Error Handling**:
- Use Django's built-in exception handling
- Return proper HTTP status codes in API responses
- Log errors appropriately
- Handle database exceptions gracefully

### Naming Conventions

**Models**: PascalCase (e.g., `ChatMessage`, `UserRoom`)  
**Views**: PascalCase with descriptive names (e.g., `MessageListView`, `RoomDetailView`)  
**Serializers**: PascalCase ending with `Serializer` (e.g., `MessageSerializer`)  
**Variables/Functions**: snake_case (e.g., `get_user_messages`, `room_id`)  
**Constants**: UPPER_SNAKE_CASE (e.g., `MAX_MESSAGE_LENGTH`)  
**URL names**: snake_case with app prefix (e.g., `chat:message-list`)

### File Organization

**App Structure**:
```
chat/
├── models.py         # Database models
├── views.py          # API views
├── serializers.py    # DRF serializers
├── urls.py           # App URL configuration
├── tests.py          # Test cases
├── admin.py          # Django admin
├── apps.py           # App configuration
└── migrations/       # Database migrations
```

**Import Order**:
```python
# Standard library
import os
from datetime import datetime

# Third-party
from rest_framework import status
from rest_framework.views import APIView

# Django
from django.db import models
from django.contrib.auth.models import User

# Local
from chat.models import Message
from .serializers import MessageSerializer
```

## Testing Guidelines

### Test Structure
- Use Django's `TestCase` class
- Create test data in `setUp()` methods
- Test both success and failure scenarios
- Use descriptive test method names

### Running Tests
```bash
# Run all tests
uv run python manage.py test

# Run specific app tests
uv run python manage.py test chat

# Run specific test class
uv run python manage.py test chat.tests.MessageViewSetTest

# Run specific test method
uv run python manage.py test chat.tests.MessageViewSetTest.test_list_messages
```

### Test Examples
```python
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class MessageAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_message(self):
        # Test message creation
        pass
```

## Database Guidelines

### Migrations
- Always create migrations after model changes: `uv run python manage.py makemigrations`
- Review generated migrations before applying
- Use descriptive migration names when needed

### Query Optimization
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many relationships
- Avoid N+1 queries in views
- Use `only()` and `defer()` for large models when appropriate

## API Design Guidelines

### REST Conventions
- Use HTTP verbs correctly (GET, POST, PUT, PATCH, DELETE)
- Return proper status codes (200, 201, 400, 401, 403, 404, 500)
- Use plural nouns for collection endpoints: `/api/messages/`
- Use singular nouns for specific resources: `/api/messages/1/`

### Response Format
- Use consistent JSON response structure
- Include error messages in responses
- Use DRF's default response format when possible

## Security Guidelines

### Authentication
- Use token-based authentication (configured with Djoser)
- Protect all API endpoints that require authentication
- Validate user permissions in views

### Data Validation
- Always validate input data in serializers
- Use Django's built-in validation
- Sanitize user input appropriately

## Development Workflow

1. Make changes to models/views/serializers
2. Create and apply migrations if needed
3. Write tests for new functionality
4. Run tests to ensure everything works
5. Test API endpoints manually if needed

## Environment Variables

Required environment variables in `.env`:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)

## Common Patterns

### Model Pattern
```python
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
```

### ViewSet Pattern
```python
from rest_framework import viewsets
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
```

### Serializer Pattern
```python
from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'content', 'created_at', 'username']
        read_only_fields = ['created_at']
```
