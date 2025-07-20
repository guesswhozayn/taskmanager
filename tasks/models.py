from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # A ForeignKey to associate each task with a specific user.
    # on_delete=models.CASCADE means if a User is deleted, all their tasks are also deleted.
    # related_name="tasks" allows us to access a user's tasks like user.tasks.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    # The main title/description of the task.
    title = models.CharField(max_length=200)

    # Optional longer description. blank=True allows the field to be empty in forms,
    # null=True allows the field to be NULL in the database.
    description = models.TextField(blank=True, null=True)

    # Boolean field to track if the task is completed or not. Default is False (incomplete).
    completed = models.BooleanField(default=False)

    # Automatically sets the creation timestamp when the task is first created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional due date for the task.
    # null=True allows it to be NULL in the DB, blank=True allows it to be empty in forms.
    due_date = models.DateTimeField(null=True, blank=True)

    # Optional priority field (e.g., 1=Low, 2=Medium, 3=High)
    # We can define choices for better clarity in forms later.
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1, blank=True, null=True)

    class Meta:
        # Order tasks by creation date by default, newest first.
        ordering = ['-created_at']

    def __str__(self):
        # This method defines how an object of this model is represented as a string.
        # Useful in the Django admin and when debugging.
        return f"{self.user.username}'s Task: {self.title} ({'Completed' if self.completed else 'Pending'})"