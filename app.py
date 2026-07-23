from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Todo App</title>
</head>

<body>

<h1>My Todo List</h1>

<form action="/add" method="post">
<input type="text" name="task" required>
<button type="submit">Add Task</button>
</form>

<hr>

<ul>

{% for task in tasks %}

<li>
{{task}}
<a href="/delete/{{loop.index0}}">Delete</a>
</li>

{% endfor %}

</ul>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    tasks.append(task)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    tasks.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)