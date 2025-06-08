# helpdesk_backend

A Django REST Framework-based backend API for a helpdesk management system with OpenAI integration for intelligent ticket processing and response generation.

## Features

- **User Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Admin, Agent, Customer)
  - User registration and profile management

- **Ticket Management**
  - Create, update, and track support tickets
  - Priority levels and status tracking
  - File attachments support
  - Ticket assignment to agents

- **AI-Powered Features**
  - OpenAI integration for automated responses
  - Intelligent ticket categorization
  - Response suggestions for agents

- **Dashboard & Analytics**
  - Real-time ticket statistics
  - Performance metrics
  - Reporting capabilities

## Tech Stack

- **Framework**: Django 4.x + Django REST Framework
- **Database**: PostgreSQL/SQLite
- **Authentication**: JWT (djangorestframework-simplejwt)
- **AI Integration**: OpenAI API
- **File Storage**: Django file handling
- **API Documentation**: Django REST Framework browsable API

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sakthi-19/helpdesk_backend.git
   cd helpdesk_backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   
   # On Windows
   env\Scripts\activate
   
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the root directory:
   ```env
   # Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Configuration
   DATABASE_URL=sqlite:///db.sqlite3
   # For PostgreSQL:
   # DATABASE_URL=postgresql://username:password@localhost:5432/helpdesk_db
   
   # OpenAI Configuration
   OPENAI_API_KEY=your-openai-api-key-here
   
   # Email Configuration (Optional)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_USE_TLS=True
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout

### Tickets
- `GET /api/tickets/` - List all tickets
- `POST /api/tickets/` - Create new ticket
- `GET /api/tickets/{id}/` - Get ticket details
- `PUT /api/tickets/{id}/` - Update ticket
- `DELETE /api/tickets/{id}/` - Delete ticket

### Users
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile
- `GET /api/users/` - List users (Admin only)

### AI Features
- `POST /api/ai/generate-response/` - Generate AI response for ticket
- `POST /api/ai/categorize-ticket/` - Auto-categorize ticket

### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics
- `GET /api/dashboard/recent-tickets/` - Get recent tickets

## Project Structure

```
helpdesk_backend/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── authentication/
│   ├── tickets/
│   ├── users/
│   ├── ai_integration/
│   └── dashboard/
├── static/
├── media/
├── requirements.txt
├── manage.py
├── .env.example
├── .gitignore
└── README.md
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `DATABASE_URL` | Database connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI features | Yes |
| `EMAIL_HOST` | SMTP server host | No |
| `EMAIL_PORT` | SMTP server port | No |
| `EMAIL_HOST_USER` | Email username | No |
| `EMAIL_HOST_PASSWORD` | Email password | No |

## Usage Examples

### Creating a Ticket
```python
import requests

url = "http://localhost:8000/api/tickets/"
headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "title": "Login Issue",
    "description": "Unable to login to the system",
    "priority": "high",
    "category": "technical"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### Generate AI Response
```python
url = "http://localhost:8000/api/ai/generate-response/"
data = {
    "ticket_id": 1,
    "context": "User cannot login to their account"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## Testing

Run tests using Django's test framework:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.tickets

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Using Docker

1. **Create Dockerfile** (if not exists):
   ```dockerfile
   FROM python:3.9
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. **Build and run**:
   ```bash
   docker build -t helpdesk-backend .
   docker run -p 8000:8000 helpdesk-backend
   ```

### Using Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```
3. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set OPENAI_API_KEY=your-openai-key
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Regularly update dependencies
- Follow Django security best practices

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@yourcompany.com or create an issue in this repository.

## Changelog

### v1.0.0
- Initial release with basic ticket management
- JWT authentication implementation
- OpenAI integration for AI responses
- Dashboard with basic analytics
