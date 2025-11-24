# Django TODO Application

A professional, full-featured TODO application built with Django 5.2 and modern Python tooling (uv). This project demonstrates best practices for Django development including CRUD operations, proper project structure, comprehensive testing, and a responsive Bootstrap UI.

## 🎯 Features

- ✅ **Create, Edit, and Delete TODOs** - Full CRUD functionality
- 📅 **Due Date Management** - Assign and track due dates
- ✔️ **Resolution Tracking** - Mark TODOs as resolved/unresolved
- ⚠️ **Overdue Detection** - Automatic visual indicators for overdue items
- 📱 **Responsive UI** - Bootstrap 5-based interface that works on all devices
- 🔍 **Admin Panel** - Built-in Django admin for data management
- ✅ **Comprehensive Tests** - 53 test cases covering all functionality
- 💾 **SQLite Database** - Zero-configuration embedded database (like H2 in Spring)

## 📋 Homework Questions Answered

This application was built to answer specific homework questions:

- **Q1: Install Django** - Command: `uv add django`
- **Q2: Register App** - File to edit: `settings.py` (INSTALLED_APPS)
- **Q3: After Creating Models** - Next step: **Run migrations** (`makemigrations` + `migrate`)
- **Q4: TODO Logic** - Goes in: `views.py`
- **Q5: Register Templates** - Location: `TEMPLATES['DIRS']` in project's settings.py
- **Q6: Run Tests** - Command: `python manage.py test`

## 🛠️ Technology Stack

- **Django 5.2.8** - High-level Python web framework
- **Python 3.12+** - Modern Python version
- **uv** - Ultra-fast Python package manager (10-100x faster than pip)
- **SQLite** - Built-in database (no external server required)
- **Bootstrap 5.3** - Responsive CSS framework
- **Django Class-Based Views** - Modern view architecture

## 📦 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- uv package manager (recommended) or pip

### Step 1: Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Clone or Navigate to Project

```bash
cd TODO_LIST
```

### Step 3: Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt  # if requirements.txt exists
# OR
pip install django
```

### Step 4: Run Database Migrations

```bash
# Using uv
uv run python manage.py migrate

# Or directly
python manage.py migrate
```

This creates the SQLite database file (`db.sqlite3`) with all necessary tables.

### Step 5: Create Admin User (Optional)

```bash
# Using uv
uv run python manage.py createsuperuser

# Or directly
python manage.py createsuperuser
```

Follow the prompts to create an admin account for accessing the admin panel at `/admin/`.

### Step 6: Run the Development Server

```bash
# Using uv
uv run python manage.py runserver

# Or directly
python manage.py runserver
```

The application will be available at:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🚀 Usage

### Creating a TODO

1. Navigate to http://127.0.0.1:8000/
2. Click the "New TODO" button
3. Fill in the form:
   - **Title** (required)
   - **Description** (optional)
   - **Due Date** (optional)
   - **Mark as Resolved** (optional checkbox)
4. Click "Create TODO"

### Editing a TODO

1. From the TODO list, click the "Edit" button on any TODO
2. Modify the fields as needed
3. Click "Update TODO"

### Deleting a TODO

1. From the TODO list, click the "Delete" button
2. Confirm the deletion on the confirmation page
3. Click "Yes, Delete This TODO"

### Quick Toggle Resolution

- Click the "✓ Resolve" or "↺ Unresolve" button to quickly toggle the status without opening the edit form

### Using the Admin Panel

1. Navigate to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Access advanced features like:
   - Bulk editing
   - Filtering by resolution status
   - Date hierarchy navigation
   - Search functionality

## 🧪 Running Tests

The application includes **53 comprehensive test cases** covering:
- Model functionality
- All CRUD operations
- Form validation
- URL routing
- Integration workflows

### Run All Tests

```bash
# Using uv
uv run python manage.py test

# Or directly
python manage.py test
```

### Run Specific Test Classes

```bash
# Test only models
python manage.py test todos.tests.TODOModelTests

# Test only views
python manage.py test todos.tests.TODOListViewTests

# Test with verbose output
python manage.py test --verbosity=2
```

### Expected Output

```
Found 53 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 0.XXXs

OK
Destroying test database for alias 'default'...
```

## 📁 Project Structure

```
TODO_LIST/
├── manage.py                 # Django management script
├── pyproject.toml           # uv project configuration
├── db.sqlite3               # SQLite database (auto-created)
├── README.md                # This file
│
├── todoproject/             # Django project settings
│   ├── settings.py          # Main settings (app registration, DB config)
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
└── todos/                   # TODO application
    ├── models.py            # TODO model definition
    ├── views.py             # CRUD views (class-based)
    ├── urls.py              # App URL routing
    ├── forms.py             # TODO form
    ├── admin.py             # Admin panel configuration
    ├── tests.py             # Comprehensive test suite (53 tests)
    ├── migrations/          # Database migrations
    │   └── 0001_initial.py
    └── templates/           # HTML templates
        └── todos/
            ├── base.html           # Base template with navbar
            ├── home.html           # TODO list view
            ├── todo_form.html      # Create/Edit form
            └── todo_confirm_delete.html  # Delete confirmation
```

## 🎨 UI Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Bootstrap Icons** - Professional SVG icons throughout
- **Visual Feedback** - Color-coded badges for status and overdue items
- **Pulsing Animation** - Overdue badges have attention-grabbing animation
- **Empty States** - Friendly messages when no TODOs exist
- **Form Validation** - Client-side and server-side validation with error messages

## 🔧 Development Commands

```bash
# Create new migrations after model changes
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Start development server
uv run python manage.py runserver

# Run tests
uv run python manage.py test

# Create superuser
uv run python manage.py createsuperuser

# Open Django shell
uv run python manage.py shell

# Check for issues
uv run python manage.py check
```

## 🗃️ Database

This application uses **SQLite** as its database:

- **Zero Configuration** - No database server setup required
- **File-Based** - Database stored in `db.sqlite3` file
- **Portable** - Entire database in a single file
- **Perfect for Development** - Like H2 database in Spring Boot

The database is automatically created when you run migrations. To start fresh:

```bash
# Delete the database file
rm db.sqlite3

# Re-run migrations
uv run python manage.py migrate

# Optionally recreate superuser
uv run python manage.py createsuperuser
```

## 📚 Learning Resources

This project demonstrates:

1. **Django Project Structure** - How apps, projects, and components fit together
2. **Models & ORM** - Database abstraction with Django's ORM
3. **Migrations** - Database schema version control
4. **Class-Based Views** - Modern Django view architecture
5. **Forms** - User input validation and processing
6. **Templates** - Template inheritance and Django template language
7. **URL Routing** - Clean URL patterns with path converters
8. **Admin Interface** - Customizing Django's built-in admin
9. **Testing** - Comprehensive test coverage with Django's test framework
10. **Modern Python Tooling** - Using uv for fast dependency management

## 🤝 Contributing

This is a learning project, but improvements are welcome! Areas to enhance:

- Add user authentication
- Implement categories/tags
- Add task priorities
- Enable task sorting/filtering
- Add API endpoints (Django REST Framework)
- Implement task search
- Add due date notifications

## 📄 License

This project is for educational purposes as part of a homework assignment.

## 🙏 Acknowledgments

- Built following Django 5.2 best practices
- Uses Context7-researched modern tooling
- Implements professional project structure
- Comprehensive test coverage

---

**Built with Django 5.2, uv, and Bootstrap 5** | Professional TODO Application for Learning
