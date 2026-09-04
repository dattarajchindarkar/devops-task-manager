import logging
from flask import Blueprint, current_app, jsonify, request

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

tasks = {}
next_task_id = 1
VALID_PRIORITIES = {"low", "medium", "high"}


@api.get("/")
def home():
    return jsonify({
        "application": current_app.config["APP_NAME"],
        "environment": current_app.config["APP_ENV"],
        "version": current_app.config["APP_VERSION"],
        "message": "Task Manager API is running"
    })


@api.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": current_app.config["APP_NAME"]
    })


@api.get("/tasks")
def list_tasks():
    return jsonify({"tasks": list(tasks.values())})


@api.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task)


@api.post("/tasks")
def create_task():
    global next_task_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "request body must be valid JSON"}), 400

    title = data.get("title")
    description = data.get("description", "")
    priority = data.get("priority", "medium")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "description must be a string"}), 400

    if priority not in VALID_PRIORITIES:
        return jsonify({
            "error": "priority must be one of: low, medium, high"
        }), 400

    task = {
        "id": next_task_id,
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "completed": False
    }

    tasks[next_task_id] = task
    logger.info("Task created: id=%s", next_task_id)
    next_task_id += 1

    return jsonify(task), 201


@api.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "request body must be valid JSON"}), 400

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({"error": "title cannot be empty"}), 400
        task["title"] = data["title"].strip()

    if "description" in data:
        if not isinstance(data["description"], str):
            return jsonify({"error": "description must be a string"}), 400
        task["description"] = data["description"].strip()

    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            return jsonify({
                "error": "priority must be one of: low, medium, high"
            }), 400
        task["priority"] = data["priority"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({"error": "completed must be a boolean"}), 400
        task["completed"] = data["completed"]

    logger.info("Task updated: id=%s", task_id)
    return jsonify(task)


@api.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404

    del tasks[task_id]
    logger.info("Task deleted: id=%s", task_id)
    return "", 204
