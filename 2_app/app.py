from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev")

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
    app.run(debug=True)
