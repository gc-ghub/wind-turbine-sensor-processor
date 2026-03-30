import subprocess
import json
import time
import os

# Config (ENV variable with default)
THRESHOLD = float(os.getenv("VIBRATION_THRESHOLD", 0.7))

def run_sensor():
    try:
        result = subprocess.run(
            ["build/sensor_simulator"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Failed to run sensor simulator: {e}")
        return None

def process_data(raw):
    try:
        data = json.loads(raw)

        # Add derived metric (example)
        data["vibration_status"] = "HIGH" if data["vibration"] > THRESHOLD else "NORMAL"

        return data

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return None

def main():
    print("🚀 Wind Turbine Sensor Monitoring Started...")
    print(f"🔧 Vibration Threshold: {THRESHOLD}")
    print("-" * 50)

    while True:
        raw = run_sensor()

        if raw:
            print(f"\n📥 Raw: {raw}")

            processed = process_data(raw)

            if processed:
                print(f"📊 Processed: {processed}")

                # Alert logic
                if processed["vibration"] > THRESHOLD:
                    print(f"⚠️ ALERT: High vibration detected! ({processed['vibration']})")

        time.sleep(2)


if __name__ == "__main__":
    main()