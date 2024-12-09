from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import basedir
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

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

@app.route("/spec")
def spec():
    swg = swagger(app)
    swg["info"]["title"] = " Додаток для контролю витрат"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"]={
        "Hello": {
            "type": "object",
            "discriminator": "helloType",
            "properties": {"message": {"type": "string"}},
            "example": {"message": "Привіт, я твій додаток для контролю витрат!"},
        },
        "ExpenseIn": {
            "type": "object",
            "discriminator": "expenseInType",
            "properties": {
                "title": {"type": "string"},
                "amount": {"type": "number"},
            },
            "example": {
                "title": "Я ваша витрата",
                "amount": 0,
            },
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                    },
                    "example": {
                        "id": 0,
                    },
                },
            ],
        },
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "Ми не змогли знайти це :("},
        },
    }
    return jsonify(swg)

swagger_ui_blueprint = get_swaggerui_blueprint("/swagger","/spec",)

app.register_blueprint(swagger_ui_blueprint)

@app.route("/")
def home():
    """
        Вітає користувача на головній сторінці
        ---
        tags:
            - домашня сторінка
        produces:
            - application/json
        responses:
              200:
                description: Привітання
                schema:
                    $ref: '#/definitions/Hello'
        """
    message = "I love you!"
    return jsonify(message=message)

@app.route("/expenses",methods=["POST"])
def create_expense():
    """
        Створює нову витрату
        ---
        tags:
            - витрати
        produces:
            - application/json
        parameters:
        - name: expense
          in: body
          description: Дані витрати
          required: true
          schema:
            $ref: '#/definitions/ExpenseIn'
        responses:
            201:
                description: Створена витрата
                schema:
                    $ref: '#/definitions/ExpenseIn'
        """
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
    """
    Повертає список усіх витрат
    ---
    tags:
        - витрати
    produces:
        - application/json
    responses:
          200:
            description: Список витрат
            schema:
                type: array
                items:
                    $ref: '#/definitions/ExpenseOut'
    """
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
    """
        Повертає одну витрату за ідентифікатором
        ---
        tags:
            - витрати
        produces:
            - application/json
        parameters:
        - name: id
          in: path
          description: Ідентифікатор витрати
          required: true
          type: number
        responses:
            200:
                description: Знайдена витрата
                schema:
                    $ref: '#/definitions/ExpenseOut'
            404:
                description: Не знайдено витрату за ідентифікатором
                schema:
                    $ref: '#/definitions/NotFound'
        """
    expense = db.get_or_404(Expense, id)
    return jsonify(
        {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
        }
    ), 200


@app.route("/expenses/<int:id>",methods=["PATCH"])
def update_expense(id):
    """
        Оновлює дані витрати за ідентифікатором
        ---
        tags:
            - витрати
        produces:
            - application/json
        parameters:
        - name: id
          in: path
          description: Ідентифікатор витрати
          required: true
          type: number
        - name: expense
          in: body
          description: Дані для оновлення витрати
          required: true
          schema:
            $ref: '#/definitions/ExpenseIn'
        responses:
            200:
                description: Оновлена витрата
                schema:
                    $ref: '#/definitions/ExpenseOut'
            404:
                description: Не знайдено витрату за ідентифікатором
                schema:
                    $ref: '#/definitions/NotFound'
        """
    expense = db.get_or_404(Expense, id)
    data = request.json
    expense.title = data.get("title",expense.title)
    expense.amount = data.get("amount", expense.amount)

    db.session.commit()

    return jsonify(
        {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
        }
    )


@app.route("/expenses/<int:id>",methods=["DELETE"])
def delete_expense(id):
    """
        Видаляє витрату за ідентифікатором
        ---
        tags:
            - витрати
        produces:
            - application/json
        parameters:
        - name: id
          in: path
          description: Ідентифікатор витрати
          required: true
          type: number
        responses:
            204:
                description: Успішне видалення витрати
            404:
                description: Не знайдено витрату за ідентифікатором
                schema:
                    $ref: '#/definitions/NotFound'
        """
    expense = db.get_or_404(Expense, id)
    Expense.query.filter_by(id=id).delete()
    db.session.commit()
    return "", 204

@app.errorhandler(404)
def handle_404(e):
    return jsonify(error="Ми не змогли знайти це :("), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
