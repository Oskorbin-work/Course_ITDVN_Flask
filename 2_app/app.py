from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  pass

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev", SQLALCHEMY_DATABASE_URI="sqlite:///expenses.sqlite3")

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column()

    def __repr__(self):
        return f"Expense(title='{self.title}', amount={self.amount})"



@app.route("/")
def home():
    message = "I love you!"
    return jsonify(message=message)

@app.route("/expenses",methods=["POST"])
def create_expense():
    pass

@app.route("/expenses",methods=["GET"])
def get_expenses():
    pass

@app.route("/expenses/<int:id>",methods=["GET"])
def get_expense(id):
    pass

@app.route("/expenses/<int:id>",methods=["PUT"])
def update_expense(id):
    pass

@app.route("/expenses/<int:id>",methods=["DELETE"])
def delete_expense(id):
    pass

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
