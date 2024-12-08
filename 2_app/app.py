from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import basedir

class Base(DeclarativeBase):
  pass


# INSERT INTO expense(title,amount) VALUES   ("Затоварка", 100);
app = Flask(__name__, instance_path=f"{basedir}/instance")
#app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev", SQLALCHEMY_DATABASE_URI="sqlite:///2_app\expenses.sqlite3")

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
    data = request.json
    new_expense = Expense(title=data['title'], amount=data["amount"])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(
        {
            "id": new_expense.id,
            "title": new_expense.title,
            "amount": new_expense.amount,
        }
    ), 201

@app.route("/test_expenses",methods=["GET"])
def create_test_expense():
    test_expense = Expense(title="Заготовка",amount=100)
    db.session.add(test_expense)
    db.session.commit()
    return jsonify(
        {
            "id": test_expense.id,
            "title": test_expense.title,
            "amount": test_expense.amount,
        }
    ), 201

@app.route("/expenses",methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    print(expenses)
    return jsonify(
        [{
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
        } for expense in expenses]
    ), 200

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
