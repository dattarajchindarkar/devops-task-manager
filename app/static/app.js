const taskList = document.getElementById("task-list");
const taskForm = document.getElementById("task-form");
const taskCount = document.getElementById("task-count");

const healthDot = document.getElementById("health-dot");
const healthText = document.getElementById("health-text");
const footerHealth = document.getElementById("footer-health");

const refreshButton = document.getElementById("refresh-button");


async function checkHealth() {
    try {
        const response = await fetch("/health");

        if (!response.ok) {
            throw new Error("Health check failed");
        }

        const data = await response.json();

        healthDot.style.background = "#12b76a";
        healthText.textContent = "API Healthy";
        footerHealth.textContent = "Online";

    } catch (error) {

        healthDot.style.background = "#f04438";
        healthText.textContent = "API Offline";
        footerHealth.textContent = "Offline";

        console.error(error);
    }
}


async function loadTasks() {

    taskList.innerHTML = `
        <div class="empty-state">
            Loading tasks...
        </div>
    `;

    try {

        const response = await fetch("/tasks");

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const data = await response.json();

        taskCount.textContent = data.tasks.length;

        renderTasks(data.tasks);

    } catch (error) {

        taskList.innerHTML = `
            <div class="empty-state">
                Failed to load tasks.
            </div>
        `;

        console.error(error);
    }
}


function renderTasks(tasks) {

    if (tasks.length === 0) {

        taskList.innerHTML = `
            <div class="empty-state">
                No tasks yet. Create your first task above.
            </div>
        `;

        return;
    }


    taskList.innerHTML = tasks.map(task => `

        <article class="task ${task.completed ? "completed" : ""}">

            <div class="task-main">

                <div class="task-title">
                    ${escapeHtml(task.title)}
                </div>

                <div class="task-description">
                    ${escapeHtml(task.description || "No description")}
                </div>

                <div class="task-meta">

                    <span class="priority">
                        ${escapeHtml(task.priority)}
                    </span>

                    <span>
                        ${task.completed ? "Completed" : "Pending"}
                    </span>

                </div>

            </div>


            <div class="task-actions">

                <button
                    class="action-button"
                    onclick="toggleTask(${task.id}, ${!task.completed})"
                >
                    ${task.completed ? "Undo" : "Complete"}
                </button>

                <button
                    class="action-button delete-button"
                    onclick="deleteTask(${task.id})"
                >
                    Delete
                </button>

            </div>

        </article>

    `).join("");
}


async function createTask(event) {

    event.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const priority = document.getElementById("priority").value;


    try {

        const response = await fetch("/tasks", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title,
                description,
                priority
            })
        });


        const data = await response.json();


        if (!response.ok) {
            alert(data.error || "Failed to create task");
            return;
        }


        taskForm.reset();

        await loadTasks();

    } catch (error) {

        alert("Unable to connect to the API.");

        console.error(error);
    }
}


async function toggleTask(taskId, completed) {

    try {

        const response = await fetch(`/tasks/${taskId}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                completed
            })
        });


        if (!response.ok) {
            throw new Error("Failed to update task");
        }


        await loadTasks();

    } catch (error) {

        alert("Failed to update task.");

        console.error(error);
    }
}


async function deleteTask(taskId) {

    const confirmed = confirm(
        "Are you sure you want to delete this task?"
    );

    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(`/tasks/${taskId}`, {
            method: "DELETE"
        });


        if (!response.ok) {
            throw new Error("Failed to delete task");
        }


        await loadTasks();

    } catch (error) {

        alert("Failed to delete task.");

        console.error(error);
    }
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


taskForm.addEventListener("submit", createTask);

refreshButton.addEventListener("click", loadTasks);


checkHealth();
loadTasks();