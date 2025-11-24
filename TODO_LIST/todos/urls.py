from django.urls import path
from . import views

urlpatterns = [
    path('', views.TODOListView.as_view(), name='todo-list'),
    path('create/', views.TODOCreateView.as_view(), name='todo-create'),
    path('<int:pk>/update/', views.TODOUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/delete/', views.TODODeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/toggle/', views.toggle_resolved, name='todo-toggle'),
]
