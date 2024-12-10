"""
Написати маленький сервіс, використовуючи GraphQL, який буде повертати JSON вигляду
{‘message’: ‘Hello World!’}.
"""
from flask import Flask, jsonify, request
import graphene
import json

app = Flask(__name__)

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, args):
        return "hello world"

schema = graphene.Schema(query=Query)

@app.route("/", methods = ['POST'])
def hello():
    data = request.get_json()
    result = schema.execute(data['query'])
    print(data['query'])

    if result.errors:
        # Handle errors appropriately, e.g., return an error response
        return jsonify({'errors': [error.message for error in result.errors]}), 400

    return jsonify(result.data["hello"])


if __name__ == '__main__':
    app.run(debug=True)


