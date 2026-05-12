import requests
try:
    import brain
    from memory import memory_manager
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    import brain
    from memory import memory_manager

from skills.registry import register_skill

@register_skill(["weather", "temperature", "forecast"])
def get_weather(command):
    """
    Fetches real-time weather data for a specified city and summarizes it with AI.
    """
    # Extract city name (default to Thrissur as requested)
    city = "Thrissur"
    cmd_lower = command.lower()
    
    # Simple extraction logic: "weather in London"
    if "in " in cmd_lower:
        city = cmd_lower.split("in ")[1].split()[0].capitalize()
    elif "for " in cmd_lower:
         city = cmd_lower.split("for ")[1].split()[0].capitalize()

    print(f"[WEATHER] Fetching data for: {city}...")
    
    try:
        # 1. Geocoding: Get coordinates for the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_res = requests.get(geo_url, timeout=5).json()
        
        if not geo_res.get('results'):
            return f"Sir, I could not locate {city} on my global maps."
            
        location = geo_res['results'][0]
        lat, lon = location['latitude'], location['longitude']
        
        # 2. Weather Forecast: Get current weather using coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url, timeout=5).json()
        
        if 'current_weather' not in weather_res:
             return f"Sir, the weather data for {city} is currently unavailable."

        current = weather_res['current_weather']
        temp = current['temperature']
        wind = current['windspeed']
        
        # 3. AI Synthesis
        history = memory_manager.get_memory(limit=3)
        prompt = f"The current weather in {city} is {temp}°C with a wind speed of {wind} km/h. Please provide a brief, professional report as Jarvis."
        
        return brain.ask_ai(prompt, history)
        
    except Exception as e:
        print(f"Weather Error: {e}")
        return "Sir, I am having trouble connecting to the meteorological satellites."
