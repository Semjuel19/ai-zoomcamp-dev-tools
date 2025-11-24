from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TODO
from .forms import TODOForm


class TODOListView(ListView):
    """Display all TODOs with filtering"""
    model = TODO
    template_name = 'todos/home.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Optional: filter by status
        show_resolved = self.request.GET.get('show_resolved', False)
        if not show_resolved:
            queryset = queryset.filter(is_resolved=False)
        return queryset


class TODOCreateView(CreateView):
    """Create new TODO"""
    model = TODO
    form_class = TODOForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')


class TODOUpdateView(UpdateView):
    """Update existing TODO"""
    model = TODO
    form_class = TODOForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')


class TODODeleteView(DeleteView):
    """Delete TODO"""
    model = TODO
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')


def toggle_resolved(request, pk):
    """Quick toggle for resolved status"""
    todo = get_object_or_404(TODO, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()
    return redirect('todo-list')
