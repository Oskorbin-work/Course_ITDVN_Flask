from flask import Flask, jsonify
import asyncio

app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=2)


async def long_running_task():
    await asyncio.sleep(5)
    return "Long task finished"


@app.route("/<int:id>")
async def index(id):
    result = await long_running_task()
    return jsonify({"request_id": id, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
