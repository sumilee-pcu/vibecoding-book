from flask import Flask, jsonify, request, render_template, abort

app = Flask(__name__)
todos = []
_next_id = 1


@app.get("/api/todos")
def list_todos():
    return jsonify(todos)


@app.post("/api/todos")
def add_todo():
    global _next_id
    data = request.get_json(force=True)
    todo = {
        "id": _next_id,
        "title": data["title"],
        "priority": data.get("priority", "보통"),
        "done": False,
    }
    todos.append(todo)
    _next_id += 1
    return jsonify(todo), 201


@app.post("/api/todos/<int:todo_id>/toggle")
def toggle_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            return jsonify(todo)
    abort(404, description="할 일을 찾을 수 없습니다")


@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return jsonify({"message": "삭제되었습니다"})
    abort(404, description="할 일을 찾을 수 없습니다")


@app.get("/")
def index():
    return render_template("index.html", todos=todos)
