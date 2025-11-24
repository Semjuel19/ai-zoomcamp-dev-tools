# Quick Start Guide - Django TODO Application

Get up and running with the TODO application in just a few simple steps!

## 🚀 Quick Start (5 minutes)

### For Users With `uv` (Recommended)

```bash
# 1. Navigate to project directory
cd TODO_LIST

# 2. Install dependencies (uv will handle virtual environment automatically)
uv sync

# 3. Run migrations (creates the SQLite database)
uv run python manage.py migrate

# 4. Start the development server
uv run python manage.py runserver

# 5. Open your browser
# Visit: http://127.0.0.1:8000/
```

That's it! You're ready to start creating TODOs!

### For Users With Standard Python/pip

```bash
# 1. Navigate to project directory
cd TODO_LIST

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv

# 3. Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# 4. Install Django
pip install django

# 5. Run migrations
python manage.py migrate

# 6. Start the development server
python manage.py runserver

# 7. Open your browser
# Visit: http://127.0.0.1:8000/
```

## 📱 Using the Application

### Main Interface
- **Home Page**: http://127.0.0.1:8000/
  - View all active TODOs
  - Create new TODO (click "+ New TODO" button)
  - Quick resolve/unresolve toggle
  - Edit or delete existing TODOs

### Admin Panel (Optional)
```bash
# First, create an admin user
uv run python manage.py createsuperuser
# OR
python manage.py createsuperuser

# Follow the prompts to set username, email, and password

# Then access admin panel at:
# http://127.0.0.1:8000/admin/
```

## ✅ Running Tests

```bash
# Run all 53 tests
uv run python manage.py test
# OR
python manage.py test

# Expected output:
# Ran 53 tests in 0.XXXs
# OK
```

## 🎯 Common Operations

### Create a TODO
1. Click "+ New TODO" button on home page
2. Fill in:
   - **Title** (required)
   - Description (optional)
   - Due Date (optional)
   - Resolved checkbox (optional)
3. Click "Create TODO"

### Edit a TODO
1. Click "Edit" button on any TODO
2. Modify fields as needed
3. Click "Update TODO"

### Delete a TODO
1. Click "Delete" button on any TODO
2. Confirm deletion on the next page
3. Click "Yes, Delete This TODO"

### Quick Toggle Resolution
- Click "✓ Resolve" to mark as complete
- Click "↺ Unresolve" to reopen

## 🔍 Features

- ✅ Full CRUD (Create, Read, Update, Delete) operations
- 📅 Optional due dates with visual overdue indicators
- ✔️ Resolution tracking (mark as complete/incomplete)
- 🎨 Responsive Bootstrap 5 UI
- 💾 SQLite database (auto-created, zero configuration)
- 🛡️ Django admin panel for advanced management
- ✅ 53 comprehensive tests

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

## 🔄 Starting Fresh

To reset the database and start over:

```bash
# Delete the database file
rm db.sqlite3

# Re-run migrations
uv run python manage.py migrate
# OR
python manage.py migrate

# Optionally recreate admin user
uv run python manage.py createsuperuser
```

## 📊 Homework Answers

This application answers specific homework questions:

| Question | Answer |
|----------|--------|
| Q1: Install Django | `uv add django` |
| Q2: File to edit for app registration | `settings.py` (INSTALLED_APPS) |
| Q3: Next step after creating models | **Run migrations** |
| Q4: Where to put TODO logic | `views.py` |
| Q5: Where to register templates | `TEMPLATES['DIRS']` in settings.py |
| Q6: Command to run tests | `python manage.py test` |

## 🆘 Troubleshooting

### Port Already in Use
If you see "Address already in use":
```bash
# Run on a different port
uv run python manage.py runserver 8001
# OR
python manage.py runserver 8001
```

### Module Not Found
If you see "No module named django":
```bash
# Make sure Django is installed
uv add django
# OR
pip install django
```

### Database Errors
If you see database errors:
```bash
# Delete database and recreate
rm db.sqlite3
uv run python manage.py migrate
```

## 📖 Full Documentation

For complete documentation, see the main `README.md` file which includes:
- Detailed installation instructions
- Technology stack explanation
- Project structure
- Development commands
- Testing guide
- And more!

## 🎓 Learning Points

This application demonstrates:
- Django 5.2 project structure
- Model-View-Template (MVT) architecture
- Class-based views
- Django ORM and migrations
- Form handling and validation
- Template inheritance
- URL routing
- Testing with Django TestCase
- SQLite embedded database
- Bootstrap UI integration

---

**Need Help?** Check the full README.md or Django documentation at https://docs.djangoproject.com/

**Enjoy managing your TODOs! 🎉**
