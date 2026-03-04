from flask import Flask, jsonify

from data_source import read_temperature_with_meta

app = Flask(__name__)


@app.get("/api/temperature")
def temperature():
    try:
        value, source, detail = read_temperature_with_meta()
        return jsonify({"temperature": value, "unit": "C", "source": source, "detail": detail})
    except RuntimeError as err:
        return jsonify({"error": str(err), "source": "serial"}), 503


@app.get("/api/status")
def status():
    return jsonify({"status": "online"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
