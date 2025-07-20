from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks import views as task_views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")), # Include URLs from 'tasks' app

    # Authentication URLs provided by Django (for login/logout)
    # We'll create our own templates for these.
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # Our custom registration view
    path("register/", task_views.register, name="register"),

    # Redirect the root URL ("/") to the task list page
    path("", include("tasks.urls")),
]