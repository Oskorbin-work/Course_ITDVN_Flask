from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.db import Expense, db
from app.schemas import expense_schema, expenses_schema

bp = Blueprint("expense", __name__, url_prefix="/expenses")

@bp.route("/",methods=["POST"])
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
    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    new_expense = Expense(title=data["title"], amount=data["amount"])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201

@bp.route("/test_expenses",methods=["GET"])
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

@bp.route("/",methods=["GET"])
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
    return jsonify(expenses_schema.dump(expenses)), 200

@bp.route("/<int:id>",methods=["GET"])
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
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>",methods=["PATCH"])
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
    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    db.session.commit()
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>",methods=["DELETE"])
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

