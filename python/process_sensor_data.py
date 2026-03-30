import subprocess
import json
import time
import os
import threading
from flask import Flask, jsonify

# ---------------- CONFIG ----------------
THRESHOLD = float(os.getenv("VIBRATION_THRESHOLD", 0.7))

# ---------------- GLOBAL STATE ----------------
latest_data = {}
app = Flask(__name__)

# ---------------- SENSOR EXECUTION ----------------
def run_sensor():
    try:
        binary_name = "sensor_simulator.exe" if os.name == "nt" else "sensor_simulator"
        exe_path = os.path.join("build", binary_name)

        result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    except Exception as e:
        print(f"❌ Failed to run sensor simulator: {e}")
        return None

# ---------------- DATA PROCESSING ----------------
def process_data(raw):
    try:
        data = json.loads(raw)

        # Add derived metric
        data["vibration_status"] = "HIGH" if data["vibration"] > THRESHOLD else "NORMAL"

        return data

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return None

# ---------------- BACKGROUND LOOP ----------------
def sensor_loop():
    global latest_data

    print("🚀 Wind Turbine Sensor Monitoring Started...")
    print(f"🔧 Vibration Threshold: {THRESHOLD}")
    print("-" * 50)

    while True:
        raw = run_sensor()

        if raw:
            print(f"\n📥 Raw: {raw}")

            processed = process_data(raw)

            if processed:
                latest_data = processed
                print(f"📊 Processed: {processed}")

                if processed["vibration"] > THRESHOLD:
                    print(f"⚠️ ALERT: High vibration detected! ({processed['vibration']})")

        time.sleep(2)

# ---------------- FLASK ROUTES ----------------
@app.route("/")
def home():
    return "🚀 Wind Turbine Sensor Service Running"

@app.route("/data")
def data():
    return jsonify(latest_data)

@app.route("/health")
def health():
    return {"status": "ok"}

# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Run background processing in separate thread
    t = threading.Thread(target=sensor_loop)
    t.daemon = True
    t.start()

    # Start Flask server
    app.run(host="0.0.0.0", port=8080)