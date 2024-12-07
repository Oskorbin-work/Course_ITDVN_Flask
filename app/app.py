from flask import Flask, render_template, request, redirect, url_for, flash

fake_db = [
    {"id": 1, "title": "Помити посуд", "completed": False},
    {"id": 2, "title": "Зробити домашнє завдання", "completed": True},
    {"id": 3, "title": "Погладити кота", "completed": False},
    {"id": 4, "title": "Вийти на прогулянку", "completed": False},
]


def get_last_todo_id():
    if len(fake_db) > 0:
        return max(todo["id"] for todo in fake_db) + 1
    else:
        return 1


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev")


@app.route("/")
def home():
    is_all_completed = all(todo["completed"] for todo in fake_db)
    return render_template(
        "base.html",
        todo_list=fake_db,
        is_all_completed=is_all_completed,
    )


@app.route("/add", methods=["POST"])
def create_todo():
    title = request.form.get("title", "").strip()
    if title:
        fake_db.append(
            {
                "id": get_last_todo_id(),
                "title": title,
                "completed": False,
            },
        )
    else:
        flash("Назва задачі не може бути порожньою!", "error")
    return redirect(url_for("home"))


@app.route("/update/<int:id>")
def update_todo(id):
    for todo in fake_db:
        if todo["id"] == id:
            todo["completed"] = not todo["completed"]
            break
    else:
        flash("Немає задачі з таким ідентифікатором", "error")
    return redirect(url_for("home"))


@app.route("/delete/<int:id>")
def delete_todo(id):
    for todo in fake_db:
        if todo["id"] == id:
            fake_db.remove(todo)
            break
    else:
        flash("Немає задачі з таким ідентифікатором", "error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
