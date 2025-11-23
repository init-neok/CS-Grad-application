# Deployment Guide

This guide covers how to set up, run, and deploy the CS Grad Application Insight Platform.

## Local Development Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- virtualenv (recommended)
- SQLite3

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CS-Grad-application
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # On Windows:
   # venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and update SECRET_KEY for production
   ```

5. **Initialize the database**
   ```bash
   # Create database with demo data
   python scripts/init_db.py --reset --with-sample

   # Or create empty database
   python scripts/init_db.py
   ```

6. **Run the development server**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   ```

   The application will be available at `http://localhost:5000`

### Demo Credentials

After running `init_db.py --with-sample`, you can log in with:
- **Email:** alice@example.com
- **Password:** pass1234

(Other demo users: bob@example.com, carol@example.com, etc.)

---

## Database

### Schema Overview

The application uses SQLite with the following main tables:

- **users** - User accounts (email, password hash)
- **profiles** - User profiles (GPA, test scores, experience)
- **educations** - Education history
- **test_scores** - Test scores (GRE, TOEFL)
- **experiences** - Work/research/internship experience
- **publications** - Academic publications
- **application_records** - Application outcomes and results

### Resetting the Database

To reset and reinitialize:
```bash
python scripts/init_db.py --reset --with-sample
```

To create a clean database:
```bash
python scripts/init_db.py --reset
```

---

## Project Structure

```
CS-Grad-application/
├── app.py                    # Flask application and models
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Home page
│   ├── auth.html           # Login/Register page
│   ├── dashboard.html      # User dashboard
│   └── explore.html        # Explore/Search page
├── static/                  # Static files
│   ├── css/
│   │   └── main.css        # Custom styles
│   └── js/
│       ├── main.js         # Global functionality (logout)
│       ├── auth.js         # Authentication handling
│       ├── dashboard.js    # Dashboard functionality
│       └── explore.js      # Search/filter functionality
├── scripts/
│   └── init_db.py          # Database initialization script
├── instance/               # Instance folder (created at runtime)
│   └── app.db             # SQLite database file
└── README.md              # Project documentation
```

---

## API Endpoints

### Authentication
- `POST /api/register` - Create new account
- `POST /api/login` - Login (creates session)
- `POST /api/logout` - Logout (clears session)

### User Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Education
- `GET /api/education` - List user's education
- `POST /api/education` - Add education
- `PUT /api/education/<id>` - Update education
- `DELETE /api/education/<id>` - Delete education

### Test Scores
- `GET /api/scores` - List test scores
- `POST /api/scores` - Add test score
- `PUT /api/scores/<id>` - Update test score
- `DELETE /api/scores/<id>` - Delete test score

### Experience
- `GET /api/experiences` - List experiences
- `POST /api/experiences` - Add experience
- `PUT /api/experiences/<id>` - Update experience
- `DELETE /api/experiences/<id>` - Delete experience

### Publications
- `GET /api/publications` - List publications
- `POST /api/publications` - Add publication
- `PUT /api/publications/<id>` - Update publication
- `DELETE /api/publications/<id>` - Delete publication

### Applications
- `GET /api/applications/my` - Get user's applications
- `POST /api/applications` - Create application record
- `PUT /api/applications/<id>` - Update application
- `DELETE /api/applications/<id>` - Delete application

### Public Search & Stats
- `GET /api/search/applications` - Search public applications
  - Query params: `university`, `program`, `country`, `degree`, `term`, `result`, `sort`, `limit`
- `GET /api/public/stats` - Get platform statistics

### Match Suggestions
- `GET /api/match/suggestions` - Get program recommendations (requires auth)

---

## Environment Configuration

### Development
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-key
```

### Production

1. **Set a strong SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Update .env:**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<generated-key-above>
   ```

3. **Use a production WSGI server** (not Flask development server):
   - Gunicorn: `pip install gunicorn && gunicorn app:app`
   - uWSGI: `pip install uwsgi && uwsgi --http :5000 --wsgi-file app.py --callable app`

4. **Set up a reverse proxy** (Nginx, Apache)

---

## Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

2. **Create Procfile:**
   ```
   web: gunicorn app:app
   ```

3. **Create requirements.txt** (already included)

4. **Deploy:**
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=<strong-key>
   git push heroku main
   heroku run python scripts/init_db.py --with-sample
   ```

### Option 2: PythonAnywhere

1. Upload your code
2. Set up a virtual environment
3. Configure WSGI application
4. Update domain/allowed hosts in config

### Option 3: DigitalOcean/AWS/Google Cloud

1. Deploy Python Flask app with:
   - Gunicorn/uWSGI as application server
   - Nginx as reverse proxy
   - Systemd or supervisor for process management
2. Use managed PostgreSQL instead of SQLite for production
3. Set up SSL with Let's Encrypt

---

## Database Migration (SQLite → PostgreSQL)

For production deployments, migrate from SQLite to PostgreSQL:

1. **Install PostgreSQL and client:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update DATABASE_URL in .env:**
   ```
   DATABASE_URL=postgresql://user:password@localhost/cs_grad_app
   ```

3. **Export SQLite data (optional):**
   ```bash
   sqlite3 instance/app.db .dump > backup.sql
   ```

4. **Create database schema in PostgreSQL:**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app('default')
   >>> with app.app_context():
   >>>     db.create_all()
   ```

---

## Monitoring & Maintenance

### Regular Tasks
- **Backup database** regularly
- **Monitor logs** for errors
- **Update dependencies** periodically
- **Check disk space** for database growth

### Performance Optimization
- Add database indices for frequently queried fields
- Implement caching for public search results
- Use pagination for large result sets (already implemented)

### Security Considerations
- Keep SECRET_KEY secret
- Use HTTPS in production
- Implement rate limiting on public APIs
- Consider adding CSRF protection for forms
- Validate and sanitize all user input

---

## Troubleshooting

### Database Issues
```bash
# Reset database completely
rm instance/app.db
python scripts/init_db.py --with-sample
```

### Port Already in Use
```bash
# Change port
flask run --port 5001
```

### Module Not Found
```bash
# Verify virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

### Secret Key Issues
```bash
# Generate new key
python -c "import secrets; print(secrets.token_hex(32))"
# Update in .env
```

---

## Support & Contribution

For issues, questions, or contributions, please open an issue or submit a pull request on the repository.
