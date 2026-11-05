import os
import sys
import requests
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION & ENVIRONMENT SETUP
# ==========================================
# Load environment variables from a local .env file (if present)
load_dotenv()

# Define the NWS station ID (Winter Haven Regional Airport - Gilbert Field)
STATION_ID = "KGIF"
# Retrieve custom location name or fallback to default
LOCATION_NAME = os.getenv("LOCATION_NAME", "Winter Haven, FL (KGIF Station)")

# NWS API requires a custom User-Agent identifying the application and contact email
HEADERS = {
    "User-Agent": "(weather-status-automator.local, platform-eng@example.com)",
    "Accept": "application/json"
}


# ==========================================
# 2. DATA INGESTION (NWS API)
# ==========================================
def fetch_exact_station_weather() -> dict:
    """Pulls live metrics directly from the specific local airport observation station."""
    obs_url = f"https://api.weather.gov/stations/{STATION_ID}/observations/latest"
    
    try:
        print(f"[*] Querying direct observation feed for station: {STATION_ID}...")
        response = requests.get(obs_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to communicate with NWS station feed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


# ==========================================
# 3. UNIT CONVERSION UTILITIES
# ==========================================
def c_to_f(celsius: float) -> float:
    """Converts Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32


# ==========================================
# 4. TELEMETRY PARSING & FORMATTING
# ==========================================
def generate_status_text(obs_data: dict) -> str:
    """Parses live station observations into a clean telemetry summary."""
    props = obs_data.get("properties", {})
    
    timestamp = props.get("timestamp", "N/A")
    text_description = props.get("textDescription", "N/A")
    
    temp_c = props.get("temperature", {}).get("value")
    humidity_val = props.get("relativeHumidity", {}).get("value")
    wind_speed_ms = props.get("windSpeed", {}).get("value")
    
    # Perform unit conversions and safe fallbacks
    temp_f = c_to_f(temp_c) if temp_c is not None else 0.0
    temp_display = f"{temp_f:.1f}°F ({temp_c}°C)" if temp_c is not None else "N/A"
    
    wind_mph = (wind_speed_ms * 2.23694) if wind_speed_ms is not None else 0.0
    humidity = round(humidity_val, 1) if humidity_val is not None else "N/A"

    status_text = (
        f"📍 DIRECT METAR STATION REPORT: {LOCATION_NAME}\n"
        f"--------------------------------------------------\n"
        f"• Condition: {text_description}\n"
        f"• Temperature: {temp_display}\n"
        f"• Humidity: {humidity}%\n"
        f"• Wind Speed: {wind_mph:.1f} mph\n"
        f"• Observation Time: {timestamp}\n"
        f"• System Status: OPTIMAL / GROUND SENSOR SYNC"
    )
    return status_text


# ==========================================
# 5. NOTIFICATION DISPATCH (DISCORD WEBHOOK)
# ==========================================
def send_discord_webhook(status_text: str):
    """Dispatches the status report securely via Discord HTTPS Webhook."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url or "api/webhooks" not in webhook_url:
        print("[*] Discord webhook URL missing or invalid in .env. Skipping remote dispatch.")
        return

    payload = {
        "content": f"```text\n{status_text}\n```"
    }

    try:
        print("[*] Pushing telemetry via HTTPS Webhook...")
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("[*] Status report successfully dispatched to Discord channel!")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to send Discord webhook: {e}", file=sys.stderr)


# ==========================================
# 6. MAIN EXECUTION FLOW
# ==========================================
if __name__ == "__main__":
    raw_data = fetch_exact_station_weather()
    formatted_text = generate_status_text(raw_data)
    
    print("\n" + formatted_text + "\n")
    
    with open("weather_status.log", "w", encoding="utf-8") as log_file:
        log_file.write(formatted_text)
    print("[*] Station report successfully written to 'weather_status.log'.")
    
    send_discord_webhook(formatted_text)