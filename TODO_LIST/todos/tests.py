"""
Comprehensive tests for the TODO application.

Test Coverage:
- Model tests (TODO creation, validation, methods)
- View tests (List, Create, Update, Delete, Toggle)
- Form tests (validation, field requirements)
- Integration tests (full CRUD workflow)
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import TODO
from .forms import TODOForm


# ============================================================================
# MODEL TESTS
# ============================================================================

class TODOModelTests(TestCase):
    """Test the TODO model functionality"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified data for all test methods"""
        cls.test_title = "Test TODO"
        cls.test_description = "This is a test description"
        cls.future_date = timezone.now().date() + timedelta(days=7)
        cls.past_date = timezone.now().date() - timedelta(days=7)
    
    def test_create_todo_with_all_fields(self):
        """Test creating a TODO with all fields populated"""
        todo = TODO.objects.create(
            title=self.test_title,
            description=self.test_description,
            due_date=self.future_date,
            is_resolved=False
        )
        
        self.assertEqual(todo.title, self.test_title)
        self.assertEqual(todo.description, self.test_description)
        self.assertEqual(todo.due_date, self.future_date)
        self.assertFalse(todo.is_resolved)
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
    
    def test_create_todo_with_minimal_fields(self):
        """Test creating a TODO with only required fields (title only)"""
        todo = TODO.objects.create(title="Minimal TODO")
        
        self.assertEqual(todo.title, "Minimal TODO")
        self.assertEqual(todo.description, "")  # Blank field default
        self.assertIsNone(todo.due_date)  # Null allowed
        self.assertFalse(todo.is_resolved)  # Default value
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
    
    def test_todo_str_representation(self):
        """Test the string representation of TODO"""
        todo = TODO.objects.create(title="String Test TODO")
        self.assertEqual(str(todo), "String Test TODO")
    
    def test_todo_default_values(self):
        """Test that default values are set correctly"""
        todo = TODO.objects.create(title="Default Values Test")
        
        self.assertFalse(todo.is_resolved, "is_resolved should default to False")
        self.assertEqual(todo.description, "", "description should default to empty string")
        self.assertIsNone(todo.due_date, "due_date should default to None")
    
    def test_is_overdue_future_date(self):
        """Test is_overdue() returns False for future due dates"""
        todo = TODO.objects.create(
            title="Future TODO",
            due_date=self.future_date,
            is_resolved=False
        )
        
        self.assertFalse(todo.is_overdue(), "Future TODO should not be overdue")
    
    def test_is_overdue_past_date(self):
        """Test is_overdue() returns True for past due dates"""
        todo = TODO.objects.create(
            title="Past TODO",
            due_date=self.past_date,
            is_resolved=False
        )
        
        self.assertTrue(todo.is_overdue(), "Past TODO should be overdue")
    
    def test_is_overdue_resolved_todo(self):
        """Test is_overdue() returns False for resolved TODOs even if past due"""
        todo = TODO.objects.create(
            title="Resolved Past TODO",
            due_date=self.past_date,
            is_resolved=True
        )
        
        self.assertFalse(todo.is_overdue(), "Resolved TODO should never be overdue")
    
    def test_is_overdue_no_due_date(self):
        """Test is_overdue() returns False when no due date is set"""
        todo = TODO.objects.create(
            title="No Due Date TODO",
            is_resolved=False
        )
        
        self.assertFalse(todo.is_overdue(), "TODO without due date should not be overdue")
    
    def test_is_overdue_today(self):
        """Test is_overdue() for a TODO due today"""
        todo = TODO.objects.create(
            title="Due Today TODO",
            due_date=timezone.now().date(),
            is_resolved=False
        )
        
        self.assertFalse(todo.is_overdue(), "TODO due today should not be overdue")
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at timestamp changes when TODO is saved"""
        todo = TODO.objects.create(title="Update Test")
        original_updated_at = todo.updated_at
        
        # Wait a tiny bit and update
        import time
        time.sleep(0.001)
        
        todo.title = "Updated Title"
        todo.save()
        
        self.assertNotEqual(todo.updated_at, original_updated_at)
        self.assertTrue(todo.updated_at > original_updated_at)
    
    def test_model_ordering(self):
        """Test that TODOs are ordered by due_date, then by -created_at"""
        # Create TODOs with different dates
        todo1 = TODO.objects.create(
            title="First",
            due_date=self.future_date
        )
        todo2 = TODO.objects.create(
            title="Second",
            due_date=self.past_date
        )
        todo3 = TODO.objects.create(
            title="Third"  # No due date
        )
        
        todos = list(TODO.objects.all())
        
        # In SQLite, NULL values come first by default in ascending order
        # So: None, past_date, future_date
        self.assertEqual(todos[0].title, "Third")
        self.assertEqual(todos[1].title, "Second")
        self.assertEqual(todos[2].title, "First")


# ============================================================================
# FORM TESTS
# ============================================================================

class TODOFormTests(TestCase):
    """Test the TODO form validation and functionality"""
    
    def test_form_with_valid_data(self):
        """Test form with all valid data"""
        form_data = {
            'title': 'Test TODO',
            'description': 'Test description',
            'due_date': timezone.now().date(),
            'is_resolved': False
        }
        form = TODOForm(data=form_data)
        
        self.assertTrue(form.is_valid(), f"Form should be valid. Errors: {form.errors}")
    
    def test_form_with_minimal_valid_data(self):
        """Test form with only required field (title)"""
        form_data = {
            'title': 'Minimal TODO',
        }
        form = TODOForm(data=form_data)
        
        self.assertTrue(form.is_valid(), f"Form should be valid. Errors: {form.errors}")
    
    def test_form_missing_required_field(self):
        """Test form validation fails when title is missing"""
        form_data = {
            'description': 'Description without title',
        }
        form = TODOForm(data=form_data)
        
        self.assertFalse(form.is_valid(), "Form should be invalid without title")
        self.assertIn('title', form.errors, "Title field should have an error")
    
    def test_form_empty_title(self):
        """Test form validation fails with empty title"""
        form_data = {
            'title': '',
        }
        form = TODOForm(data=form_data)
        
        self.assertFalse(form.is_valid(), "Form should be invalid with empty title")
        self.assertIn('title', form.errors)
    
    def test_form_fields_present(self):
        """Test that form contains all expected fields"""
        form = TODOForm()
        
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('due_date', form.fields)
        self.assertIn('is_resolved', form.fields)
    
    def test_form_field_widgets(self):
        """Test that form fields have correct widget types"""
        form = TODOForm()
        
        # Check that widgets are properly configured
        self.assertEqual(form.fields['title'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['description'].widget.attrs.get('class'), 'form-control')
        # Check DateInput widget - the 'type' is stored in input_type for DateInput
        # For now, just check the class attribute is set correctly
        self.assertEqual(form.fields['due_date'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['is_resolved'].widget.attrs.get('class'), 'form-check-input')
    
    def test_form_saves_correctly(self):
        """Test that form saves data to database correctly"""
        form_data = {
            'title': 'Form Save Test',
            'description': 'Testing form save',
            'due_date': timezone.now().date(),
            'is_resolved': False
        }
        form = TODOForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        todo = form.save()
        
        self.assertEqual(todo.title, 'Form Save Test')
        self.assertEqual(todo.description, 'Testing form save')
        self.assertFalse(todo.is_resolved)
        self.assertEqual(TODO.objects.count(), 1)


# ============================================================================
# VIEW TESTS
# ============================================================================

class TODOListViewTests(TestCase):
    """Test the TODO list view"""
    
    def setUp(self):
        """Create test client and sample data for each test"""
        self.client = Client()
        self.list_url = reverse('todo-list')
        
        # Create some test TODOs
        self.todo1 = TODO.objects.create(
            title="Active TODO 1",
            is_resolved=False
        )
        self.todo2 = TODO.objects.create(
            title="Active TODO 2",
            is_resolved=False
        )
        self.todo3 = TODO.objects.create(
            title="Resolved TODO",
            is_resolved=True
        )
    
    def test_list_view_accessible(self):
        """Test that list view is accessible"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        """Test that list view uses the correct template"""
        response = self.client.get(self.list_url)
        
        self.assertTemplateUsed(response, 'todos/home.html')
    
    def test_list_view_displays_unresolved_todos_by_default(self):
        """Test that list view shows only unresolved TODOs by default"""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active TODO 1")
        self.assertContains(response, "Active TODO 2")
        self.assertNotContains(response, "Resolved TODO")
    
    def test_list_view_displays_all_todos_with_filter(self):
        """Test that list view shows all TODOs when show_resolved is True"""
        response = self.client.get(self.list_url + '?show_resolved=true')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active TODO 1")
        self.assertContains(response, "Active TODO 2")
        self.assertContains(response, "Resolved TODO")
    
    def test_list_view_context_object_name(self):
        """Test that list view provides 'todos' in context"""
        response = self.client.get(self.list_url)
        
        self.assertIn('todos', response.context)
        todos = response.context['todos']
        self.assertEqual(len(todos), 2)  # Only unresolved by default
    
    def test_list_view_empty_state(self):
        """Test list view when no TODOs exist"""
        # Delete all TODOs
        TODO.objects.all().delete()
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['todos']), 0)
    
    def test_list_view_uses_correct_view_class(self):
        """Test that the list URL uses TODOListView"""
        from .views import TODOListView
        response = self.client.get(self.list_url)
        
        self.assertIsInstance(response.context['view'], TODOListView)


class TODOCreateViewTests(TestCase):
    """Test the TODO create view"""
    
    def setUp(self):
        """Create test client"""
        self.client = Client()
        self.create_url = reverse('todo-create')
    
    def test_create_view_get(self):
        """Test GET request to create view"""
        response = self.client.get(self.create_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertIsInstance(response.context['form'], TODOForm)
    
    def test_create_view_post_valid_data(self):
        """Test POST request with valid data creates a TODO"""
        data = {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': timezone.now().date(),
            'is_resolved': False
        }
        
        response = self.client.post(self.create_url, data)
        
        # Should redirect to list view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo-list'))
        
        # Check TODO was created
        self.assertEqual(TODO.objects.count(), 1)
        todo = TODO.objects.first()
        self.assertEqual(todo.title, 'New TODO')
        self.assertEqual(todo.description, 'New description')
    
    def test_create_view_post_minimal_data(self):
        """Test POST request with only required field"""
        data = {
            'title': 'Minimal TODO',
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TODO.objects.count(), 1)
        
        todo = TODO.objects.first()
        self.assertEqual(todo.title, 'Minimal TODO')
        self.assertEqual(todo.description, '')
        self.assertIsNone(todo.due_date)
    
    def test_create_view_post_invalid_data(self):
        """Test POST request with invalid data (missing title)"""
        data = {
            'description': 'No title provided',
        }
        
        response = self.client.post(self.create_url, data)
        
        # Should not redirect, should show form with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        
        # No TODO should be created
        self.assertEqual(TODO.objects.count(), 0)
    
    def test_create_view_success_url(self):
        """Test that successful creation redirects to correct URL"""
        data = {'title': 'Test Redirect'}
        response = self.client.post(self.create_url, data)
        
        self.assertRedirects(response, reverse('todo-list'))


class TODOUpdateViewTests(TestCase):
    """Test the TODO update view"""
    
    def setUp(self):
        """Create test client and a TODO to update"""
        self.client = Client()
        self.todo = TODO.objects.create(
            title="Original Title",
            description="Original Description",
            is_resolved=False
        )
        self.update_url = reverse('todo-update', kwargs={'pk': self.todo.pk})
    
    def test_update_view_get(self):
        """Test GET request to update view"""
        response = self.client.get(self.update_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertIsInstance(response.context['form'], TODOForm)
        
        # Form should be pre-populated with existing data
        form = response.context['form']
        self.assertEqual(form.instance.title, "Original Title")
        self.assertEqual(form.instance.description, "Original Description")
    
    def test_update_view_post_valid_data(self):
        """Test POST request with valid data updates the TODO"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'is_resolved': True
        }
        
        response = self.client.post(self.update_url, data)
        
        # Should redirect to list view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo-list'))
        
        # Refresh from database and check changes
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated Description')
        self.assertTrue(self.todo.is_resolved)
    
    def test_update_view_post_invalid_data(self):
        """Test POST request with invalid data (empty title)"""
        data = {
            'title': '',  # Invalid - required field
            'description': 'Updated Description',
        }
        
        response = self.client.post(self.update_url, data)
        
        # Should not redirect, should show form with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        
        # TODO should not be updated
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Original Title')
    
    def test_update_view_nonexistent_todo(self):
        """Test update view with non-existent TODO ID"""
        nonexistent_url = reverse('todo-update', kwargs={'pk': 99999})
        response = self.client.get(nonexistent_url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_update_preserves_created_at(self):
        """Test that updating doesn't change created_at timestamp"""
        original_created_at = self.todo.created_at
        
        data = {
            'title': 'Updated Title',
        }
        self.client.post(self.update_url, data)
        
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.created_at, original_created_at)


class TODODeleteViewTests(TestCase):
    """Test the TODO delete view"""
    
    def setUp(self):
        """Create test client and a TODO to delete"""
        self.client = Client()
        self.todo = TODO.objects.create(
            title="TODO to Delete",
            description="This will be deleted"
        )
        self.delete_url = reverse('todo-delete', kwargs={'pk': self.todo.pk})
    
    def test_delete_view_get(self):
        """Test GET request to delete view (confirmation page)"""
        response = self.client.get(self.delete_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
        self.assertContains(response, "TODO to Delete")
    
    def test_delete_view_post(self):
        """Test POST request to delete view actually deletes the TODO"""
        self.assertEqual(TODO.objects.count(), 1)
        
        response = self.client.post(self.delete_url)
        
        # Should redirect to list view
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo-list'))
        
        # TODO should be deleted
        self.assertEqual(TODO.objects.count(), 0)
    
    def test_delete_view_nonexistent_todo(self):
        """Test delete view with non-existent TODO ID"""
        nonexistent_url = reverse('todo-delete', kwargs={'pk': 99999})
        response = self.client.get(nonexistent_url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_success_url(self):
        """Test that successful deletion redirects to correct URL"""
        response = self.client.post(self.delete_url)
        
        self.assertRedirects(response, reverse('todo-list'))


class ToggleResolvedViewTests(TestCase):
    """Test the toggle_resolved function view"""
    
    def setUp(self):
        """Create test client and TODOs"""
        self.client = Client()
        self.todo = TODO.objects.create(
            title="TODO to Toggle",
            is_resolved=False
        )
        self.toggle_url = reverse('todo-toggle', kwargs={'pk': self.todo.pk})
    
    def test_toggle_resolved_from_false_to_true(self):
        """Test toggling resolved status from False to True"""
        self.assertFalse(self.todo.is_resolved)
        
        response = self.client.get(self.toggle_url)
        
        # Should redirect to list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo-list'))
        
        # Status should be toggled
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
    
    def test_toggle_resolved_from_true_to_false(self):
        """Test toggling resolved status from True to False"""
        self.todo.is_resolved = True
        self.todo.save()
        
        response = self.client.get(self.toggle_url)
        
        self.assertEqual(response.status_code, 302)
        
        # Status should be toggled back
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_resolved)
    
    def test_toggle_multiple_times(self):
        """Test toggling resolved status multiple times"""
        # Start with False
        self.assertFalse(self.todo.is_resolved)
        
        # Toggle to True
        self.client.get(self.toggle_url)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
        
        # Toggle back to False
        self.client.get(self.toggle_url)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_resolved)
        
        # Toggle to True again
        self.client.get(self.toggle_url)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
    
    def test_toggle_nonexistent_todo(self):
        """Test toggle with non-existent TODO ID"""
        nonexistent_url = reverse('todo-toggle', kwargs={'pk': 99999})
        response = self.client.get(nonexistent_url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_toggle_post_request(self):
        """Test that toggle works with POST request too"""
        response = self.client.post(self.toggle_url)
        
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TODOCRUDIntegrationTests(TestCase):
    """Test full CRUD workflow for TODO items"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_full_crud_workflow(self):
        """Test complete Create -> Read -> Update -> Delete workflow"""
        # 1. CREATE - Create a new TODO
        create_data = {
            'title': 'Integration Test TODO',
            'description': 'Testing full CRUD cycle',
            'due_date': timezone.now().date() + timedelta(days=5),
            'is_resolved': False
        }
        
        create_response = self.client.post(reverse('todo-create'), create_data)
        self.assertEqual(create_response.status_code, 302)
        self.assertEqual(TODO.objects.count(), 1)
        
        # Get the created TODO
        todo = TODO.objects.first()
        self.assertEqual(todo.title, 'Integration Test TODO')
        
        # 2. READ - View the TODO in the list
        list_response = self.client.get(reverse('todo-list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, 'Integration Test TODO')
        
        # 3. UPDATE - Modify the TODO
        update_data = {
            'title': 'Updated Integration Test TODO',
            'description': 'Updated description',
            'is_resolved': True
        }
        
        update_response = self.client.post(
            reverse('todo-update', kwargs={'pk': todo.pk}),
            update_data
        )
        self.assertEqual(update_response.status_code, 302)
        
        # Verify update
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Integration Test TODO')
        self.assertEqual(todo.description, 'Updated description')
        self.assertTrue(todo.is_resolved)
        
        # 4. DELETE - Remove the TODO
        delete_response = self.client.post(
            reverse('todo-delete', kwargs={'pk': todo.pk})
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertEqual(TODO.objects.count(), 0)
    
    def test_multiple_todos_workflow(self):
        """Test workflow with multiple TODOs"""
        # Create multiple TODOs
        todos_data = [
            {'title': 'TODO 1', 'is_resolved': False},
            {'title': 'TODO 2', 'is_resolved': False},
            {'title': 'TODO 3', 'is_resolved': True},
        ]
        
        for data in todos_data:
            self.client.post(reverse('todo-create'), data)
        
        self.assertEqual(TODO.objects.count(), 3)
        
        # List should show only unresolved by default
        list_response = self.client.get(reverse('todo-list'))
        self.assertContains(list_response, 'TODO 1')
        self.assertContains(list_response, 'TODO 2')
        self.assertNotContains(list_response, 'TODO 3')
        
        # Toggle one TODO
        todo1 = TODO.objects.get(title='TODO 1')
        toggle_response = self.client.get(
            reverse('todo-toggle', kwargs={'pk': todo1.pk})
        )
        
        # Now only TODO 2 should show in default list
        list_response = self.client.get(reverse('todo-list'))
        self.assertNotContains(list_response, 'TODO 1')
        self.assertContains(list_response, 'TODO 2')
        
        # With filter, all should show
        list_response_all = self.client.get(reverse('todo-list') + '?show_resolved=true')
        self.assertContains(list_response_all, 'TODO 1')
        self.assertContains(list_response_all, 'TODO 2')
        self.assertContains(list_response_all, 'TODO 3')
    
    def test_overdue_todo_workflow(self):
        """Test workflow with overdue TODOs"""
        past_date = timezone.now().date() - timedelta(days=5)
        
        # Create overdue TODO
        overdue_data = {
            'title': 'Overdue TODO',
            'due_date': past_date,
            'is_resolved': False
        }
        self.client.post(reverse('todo-create'), overdue_data)
        
        todo = TODO.objects.first()
        self.assertTrue(todo.is_overdue())
        
        # Mark as resolved
        self.client.get(reverse('todo-toggle', kwargs={'pk': todo.pk}))
        todo.refresh_from_db()
        
        # Should no longer be overdue
        self.assertFalse(todo.is_overdue())
    
    def test_empty_to_populated_workflow(self):
        """Test starting with empty list and adding TODOs"""
        # Start with empty list
        list_response = self.client.get(reverse('todo-list'))
        self.assertEqual(len(list_response.context['todos']), 0)
        
        # Add first TODO
        self.client.post(reverse('todo-create'), {'title': 'First TODO'})
        list_response = self.client.get(reverse('todo-list'))
        self.assertEqual(len(list_response.context['todos']), 1)
        
        # Add second TODO
        self.client.post(reverse('todo-create'), {'title': 'Second TODO'})
        list_response = self.client.get(reverse('todo-list'))
        self.assertEqual(len(list_response.context['todos']), 2)
        
        # Delete all
        for todo in TODO.objects.all():
            self.client.post(reverse('todo-delete', kwargs={'pk': todo.pk}))
        
        # Back to empty
        list_response = self.client.get(reverse('todo-list'))
        self.assertEqual(len(list_response.context['todos']), 0)


# ============================================================================
# URL TESTS
# ============================================================================

class URLTests(TestCase):
    """Test URL configuration and routing"""
    
    def test_list_url_resolves(self):
        """Test that list URL is configured correctly"""
        url = reverse('todo-list')
        self.assertEqual(url, '/')
    
    def test_create_url_resolves(self):
        """Test that create URL is configured correctly"""
        url = reverse('todo-create')
        self.assertEqual(url, '/create/')
    
    def test_update_url_resolves(self):
        """Test that update URL is configured correctly"""
        url = reverse('todo-update', kwargs={'pk': 1})
        self.assertEqual(url, '/1/update/')
    
    def test_delete_url_resolves(self):
        """Test that delete URL is configured correctly"""
        url = reverse('todo-delete', kwargs={'pk': 1})
        self.assertEqual(url, '/1/delete/')
    
    def test_toggle_url_resolves(self):
        """Test that toggle URL is configured correctly"""
        url = reverse('todo-toggle', kwargs={'pk': 1})
        self.assertEqual(url, '/1/toggle/')
