from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=2)


def long_running_task():
    time.sleep(5)
    return "Long task finished"


@app.route("/<int:id>")
def index(id):
    future = executor.submit(long_running_task)
    result = future.result()
    return jsonify({"request_id": id, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
