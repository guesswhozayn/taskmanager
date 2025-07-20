function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to handle toggling task completion status via AJAX
async function toggleComplete(taskId) {
    const url = `/tasks/toggle/${taskId}/`;
    const csrfToken = getCookie('csrftoken');

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json' // Indicate we're sending JSON (optional for this simple POST)
            },
            // body: JSON.stringify({}) // No body needed for a simple toggle, but good to know
        });

        if (!response.ok) {
            // Handle HTTP errors (e.g., 404, 500)
            const errorData = await response.json();
            console.error('Error toggling task:', errorData.error);
            alert('Error toggling task: ' + errorData.error);
            return; // Stop execution
        }

        const data = await response.json();
        console.log('Toggle response:', data);

        // Update UI dynamically
        const taskItem = document.getElementById(`task-item-${taskId}`);
        const taskTitle = taskItem.querySelector(`.task-title-${taskId}`);
        const checkbox = taskItem.querySelector('.task-checkbox');

        if (data.completed) {
            taskItem.classList.remove('list-group-item-light');
            taskItem.classList.add('list-group-item-success');
            taskTitle.classList.add('text-decoration-line-through');
            checkbox.checked = true;
        } else {
            taskItem.classList.remove('list-group-item-success');
            taskItem.classList.add('list-group-item-light');
            taskTitle.classList.remove('text-decoration-line-through');
            checkbox.checked = false;
        }

    } catch (error) {
        console.error('Network or parsing error:', error);
        alert('An unexpected error occurred.');
    }
}

// Function to handle deleting a task via AJAX
async function deleteTask(taskId) {
    if (!confirm("Are you sure you want to delete this task? This action cannot be undone.")) {
        return; // User cancelled
    }

    const url = `/tasks/delete/${taskId}/`;
    const csrfToken = getCookie('csrftoken');

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error deleting task:', errorData.error);
            alert('Error deleting task: ' + errorData.error);
            return;
        }

        const data = await response.json();
        console.log('Delete response:', data);

        // Remove the task item from the UI
        const taskItem = document.getElementById(`task-item-${taskId}`);
        if (taskItem) {
            taskItem.remove(); // Removes the element from the DOM
            // Optional: Check if the list is now empty and display 'no tasks' message
            const taskList = document.getElementById('task-list');
            if (taskList && taskList.children.length === 0) {
                const container = taskList.parentElement; // Get parent of the ul
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-info';
                alertDiv.setAttribute('role', 'alert');
                alertDiv.textContent = "You don't have any tasks yet. Add one above!";
                taskList.remove(); // Remove the empty ul
                container.appendChild(alertDiv);
            }
        }

    } catch (error) {
        console.error('Network or parsing error:', error);
        alert('An unexpected error occurred during deletion.');
    }
}

// Attach event listeners after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Event listener for checkboxes
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (event) => {
            const taskId = event.target.dataset.taskId;
            toggleComplete(taskId);
        });
    });

    // Event listener for delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            const taskId = event.target.dataset.taskId;
            deleteTask(taskId);
        });
    });
});