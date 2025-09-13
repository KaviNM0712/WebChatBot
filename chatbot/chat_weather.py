import requests
import subprocess

# ===============================
# CONFIG
# ===============================

# Your Tomorrow.io API key
TOMORROW_API_KEY = "tlhZDKRmL6aSY7w5YFvmgm95eyBrXYnG"

# Ollama model name (use "llama3" or "deepseek")
MODEL_NAME = "llama3"


# ===============================
# WEATHER FUNCTION
# ===============================

def get_weather(city: str):
    """Fetch real-time weather from Tomorrow.io"""
    url = "https://api.tomorrow.io/v4/weather/realtime"
    params = {"location": city, "apikey": TOMORROW_API_KEY}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code == 200:
        data = r.json()
        values = data.get("data", {}).get("values", {})
        return (
            f"City: {city}\n"
            f"Temperature: {values.get('temperature')}°C\n"
            f"Humidity: {values.get('humidity')}%\n"
            f"Wind Speed: {values.get('windSpeed')} m/s\n"
        )
    else:
        return f"Error from API: {r.status_code} {r.text}"


# ===============================
# PROMPT BUILDER
# ===============================

SYSTEM_PROMPT = "You are a helpful and friendly assistant. Answer clearly and conversationally."

def build_prompt(user_message: str, tool_result: str = None):
    if tool_result:
        return f"{SYSTEM_PROMPT}\n\nWeather data:\n{tool_result}\n\nUser: {user_message}\nAssistant:"
    else:
        return f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"


# ===============================
# OLLAMA RUNNER (STREAMING)
# ===============================

def run_ollama(prompt: str, model: str = MODEL_NAME):
    """Send prompt to Ollama model and stream response live"""
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    output = []
    # Write the prompt
    process.stdin.write(prompt)
    process.stdin.close()

    # Read line by line (streaming)
    for line in process.stdout:
        print(line, end="")   # print live to console
        output.append(line)

    process.wait()
    return "".join(output).strip()


# ===============================
# MAIN CHAT LOOP
# ===============================

if __name__ == "__main__":
    user_q = input("You: ")

    # Simple rule: if user asks about weather, call API
    if "weather" in user_q.lower() or "temperature" in user_q.lower():
        city = "Delhi"  # <-- change default city or add parser later
        tool_result = get_weather(city)
        prompt = build_prompt(user_q, tool_result)
    else:
        prompt = build_prompt(user_q)

    print("\nAssistant: ", end="")
    reply = run_ollama(prompt)
    print()  # newline after reply
