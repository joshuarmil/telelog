import time
import requests
from datetime import datetime, timezone

BASE_URL = "http://localhost:8000"

def run_simulation():
    print("Starting Distributed IoT Hardware Simulator\n")

    # =========================================================================
    # STEP 1: AUTOMATIC NODE PROVISIONING
    # =========================================================================
    device_payload = {
        "name": "Gardenia-jasminoides-01",
        "location": "Dining-Room"
    }
    
    try:
        print("Attempting to provision test device via API gateway")
        response = requests.post(f'{BASE_URL}/devices', json=device_payload)
        response.raise_for_status()
        device = response.json()
        device_id = device["id"]
        print(f'Device provisioned successfully. Assigned ID: {device_id}\n')
    except Exception as e:
        print(f'Failed to reach gateway at {BASE_URL}. Ensure FastAPI server is running!')
        print(f'Error: {str(e)}')
        return

    # Helper function to fire ingest packets easily
    def inject_reading(temp: float, voltage: float, label: str):
        payload = {
            "device_id": device_id,
            "temperature": temp,
            "battery_voltage": voltage,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        print(f'[{label}] Sending: {temp}°C | {voltage}V')
        res = requests.post(f"{BASE_URL}/telemetry/", json=payload)
        res.raise_for_status()
        time.sleep(0.4) # Brief delay between bursts

    # =========================================================================
    # STEP 2: PHASES SIMULATION RUNTIME
    # =========================================================================
    print("Phase 1: Simulating baseline healthy operational status")
    inject_reading(temp=24.2, voltage=3.62, label="NORMAL")
    inject_reading(temp=25.5, voltage=3.61, label="NORMAL")
    inject_reading(temp=24.8, voltage=3.59, label="NORMAL")
    
    print("\nPhase 2: Triggering critical temperature warning")
    inject_reading(temp=45.0, voltage=3.55, label="HEATING")
    inject_reading(temp=88.4, voltage=3.52, label="CRITICAL OVERHEAT")
    inject_reading(temp=92.1, voltage=3.50, label="CRITICAL OVERHEAT")
    
    print("\nPhase 3: Simulating battery warning")
    inject_reading(temp=32.0, voltage=2.85, label="LOW BATTERY")
    inject_reading(temp=28.4, voltage=2.10, label="CRITICAL VOLTAGE")

    print("\nSimulation packet blast completed successfully")

if __name__ == "__main__":
    run_simulation()
