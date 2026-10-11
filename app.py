
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
tasks = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>My To-Do App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f4f8;
            padding: 30px 15px;
        }
        .container {
            max-width: 550px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        h1 { text-align: center; color: #24476b; }
        form.add { display: flex; gap: 8px; }
        input[type=text] {
            flex: 1;
            min-width: 0;
            padding: 12px;
        }
        button {
            padding: 10px;
            border: 0;
            border-radius: 5px;
            cursor: pointer;
            color: white;
            background: #2474c6;
        }
        ul { padding: 0; list-style: none; }
        li {
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .task { flex: 1; overflow-wrap: anywhere; }
        .done { text-decoration: line-through; color: gray; }
        .delete { background: #d83b45; }
        .complete { background: #238636; }
    </style>
</head>
<body>
<div class="container">
    <h1>My To-Do List</h1>
    <form class="add" method="POST" action="/add">
        <input type="text" name="task"
               placeholder="Enter a new task..." required>
        <button type="submit">Add</button>
    </form>
    <h3>My Tasks ({{ tasks|length }})</h3>
    <ul>
    {% for task in tasks %}
        <li>
            <span class="task {{ 'done' if task.done else '' }}">
                {{ task.title }}
            </span>
            <form method="POST" action="/complete/{{ task.id }}">
                <button class="complete" type="submit">
                    {{ 'Undo' if task.done else 'Done' }}
                </button>
            </form>
            <form method="POST" action="/delete/{{ task.id }}">
                <button class="delete" type="submit">Delete</button>
            </form>
        </li>
    {% else %}
        <li>No tasks yet. Add your first task!</li>
    {% endfor %}
    </ul>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("task", "").strip()
    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "done": False
        })
        next_id += 1
    return redirect("/")

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)