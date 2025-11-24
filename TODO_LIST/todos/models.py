from django.db import models
from django.utils import timezone


class TODO(models.Model):
    """
    Model representing a TODO item.
    
    Features:
    - Title and optional description
    - Due date tracking
    - Resolution status
    - Automatic timestamp tracking
    """
    
    title = models.CharField(max_length=200, help_text="TODO title")
    description = models.TextField(blank=True, help_text="Detailed description")
    due_date = models.DateField(null=True, blank=True, help_text="When is this due?")
    is_resolved = models.BooleanField(default=False, help_text="Is this completed?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-created_at']
        verbose_name = "TODO"
        verbose_name_plural = "TODOs"
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Check if TODO is overdue"""
        if self.due_date and not self.is_resolved:
            return self.due_date < timezone.now().date()
        return False
