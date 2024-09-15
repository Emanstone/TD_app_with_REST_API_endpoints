from django.urls import path
from . import views


urlpatterns = [
    path('todos/', views.TodoListCreate.as_view()),
    path('todos/<int:pk>/', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoComplete.as_view()),
    path('todos/completed/', views.TodoCompletedList.as_view()),
    path('todos/completed/<int:pk>/', views.TodoUnComplete.as_view()),

    # Authentication
    path('signup', views.signup),
    path('login', views.login),
]

