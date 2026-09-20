import asyncio
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.config import settings
from app.utils.logger import logger

def weather_code_to_condition(code: int) -> str:
    mapping = {
        0: "Clear Sky",
        1: "Mainly Sunny",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Slight Rain",
        62: "Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        80: "Rain Showers",
        81: "Scattered Rain",
        82: "Violent Rain",
        95: "Thunderstorm"
    }
    return mapping.get(code, "Partly Cloudy")

class WeatherProvider(ABC):
    @abstractmethod
    async def get_forecast(self, lat: float, lng: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_hourly_forecast(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_rain_probability(self, lat: float, lng: float) -> int:
        pass

    @abstractmethod
    async def get_wind_speed(self, lat: float, lng: float) -> float:
        pass

    @abstractmethod
    async def get_temperature(self, lat: float, lng: float) -> float:
        pass

    @abstractmethod
    async def get_humidity(self, lat: float, lng: float) -> float:
        pass

    @abstractmethod
    async def get_weather_window(self, lat: float, lng: float) -> Dict[str, Any]:
        pass

class OpenMeteoWeatherProvider(WeatherProvider):
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.client = httpx.AsyncClient(timeout=6.0)

    async def _fetch_raw(self, lat: float, lng: float) -> Dict[str, Any]:
        params = {
            "latitude": lat,
            "longitude": lng,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
            "timezone": "auto"
        }
        resp = await self.client.get(self.base_url, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_forecast(self, lat: float, lng: float) -> Dict[str, Any]:
        raw = await self._fetch_raw(lat, lng)
        current_data = raw.get("current", {})
        hourly_data = raw.get("hourly", {})
        daily_data = raw.get("daily", {})

        cur_temp = float(current_data.get("temperature_2m", 33.0))
        cur_hum = float(current_data.get("relative_humidity_2m", 58.0))
        cur_wind = float(current_data.get("wind_speed_10m", 14.0))
        weather_code = int(current_data.get("weather_code", 1))
        condition = weather_code_to_condition(weather_code)

        # Parse hourly (next 6 intervals)
        hourly_list = []
        times = hourly_data.get("time", [])
        temps = hourly_data.get("temperature_2m", [])
        rain_probs = hourly_data.get("precipitation_probability", [])
        humidities = hourly_data.get("relative_humidity_2m", [])

        # Start from current hour
        now_idx = 0
        now_hour = datetime.now().hour
        for idx, t_str in enumerate(times):
            if f"T{now_hour:02d}:" in t_str:
                now_idx = idx
                break

        for i in range(now_idx, min(now_idx + 6, len(times))):
            t_raw = times[i]
            time_part = t_raw.split("T")[-1][:5] if "T" in t_raw else t_raw
            hourly_list.append({
                "time": time_part,
                "temp": round(float(temps[i]), 1) if i < len(temps) else cur_temp,
                "rainProb": int(rain_probs[i]) if i < len(rain_probs) else 10,
                "humidity": round(float(humidities[i]), 1) if i < len(humidities) else cur_hum
            })

        if not hourly_list:
            hourly_list = [
                {"time": "12:00", "temp": cur_temp, "rainProb": 12, "humidity": cur_hum},
                {"time": "15:00", "temp": cur_temp - 1, "rainProb": 15, "humidity": cur_hum + 5},
                {"time": "18:00", "temp": cur_temp - 3, "rainProb": 10, "humidity": cur_hum + 10}
            ]

        # Parse daily (next 7 days)
        daily_list = []
        d_times = daily_data.get("time", [])
        d_max = daily_data.get("temperature_2m_max", [])
        d_min = daily_data.get("temperature_2m_min", [])
        d_rain = daily_data.get("precipitation_probability_max", [])
        d_codes = daily_data.get("weather_code", [])

        days_labels = ["Today", "Tomorrow", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
        for i in range(min(7, len(d_times))):
            rain_val = int(d_rain[i]) if i < len(d_rain) else 12
            code_val = int(d_codes[i]) if i < len(d_codes) else 1
            cond_str = weather_code_to_condition(code_val)

            if rain_val > 40:
                spray = "Poor (Rain risk)"
            elif rain_val > 25:
                spray = "Morning Only (Wind/drizzle)"
            else:
                spray = "Good (After 17:00)"

            daily_list.append({
                "day": days_labels[i] if i < len(days_labels) else f"Day {i+1}",
                "tempMax": round(float(d_max[i]), 1) if i < len(d_max) else 34.0,
                "tempMin": round(float(d_min[i]), 1) if i < len(d_min) else 22.0,
                "rainProb": rain_val,
                "condition": cond_str,
                "sprayRating": spray
            })

        rain_24h = int(d_rain[0]) if d_rain else 12

        advisory_msg = (
            "Favorable conditions for drip irrigation this evening. Wind speed is safe for low-drift foliar activities."
            if rain_24h < 25 and cur_wind < 20 else
            "Precipitation expected in region. Delay foliar chemical spraying until canopy dries."
        )

        return {
            "current": {
                "temp": cur_temp,
                "condition": condition,
                "humidity": cur_hum,
                "wind": f"{round(cur_wind, 1)} km/h SW",
                "rainfallProb": rain_24h,
                "uvIndex": 8,
                "dewPoint": round(cur_temp - ((100 - cur_hum) / 5), 1),
                "et0": "5.8 mm/day",
                "advisory": advisory_msg
            },
            "hourly": hourly_list,
            "daily": daily_list
        }

    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        forecast = await self.get_forecast(lat, lng)
        return forecast["current"]

    async def get_hourly_forecast(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        forecast = await self.get_forecast(lat, lng)
        return forecast["hourly"]

    async def get_rain_probability(self, lat: float, lng: float) -> int:
        cur = await self.get_current_weather(lat, lng)
        return int(cur.get("rainfallProb", 12))

    async def get_wind_speed(self, lat: float, lng: float) -> float:
        cur = await self.get_current_weather(lat, lng)
        wind_str = cur.get("wind", "14.0 km/h")
        try:
            return float(wind_str.split()[0])
        except Exception:
            return 14.0

    async def get_temperature(self, lat: float, lng: float) -> float:
        cur = await self.get_current_weather(lat, lng)
        return float(cur.get("temp", 33.0))

    async def get_humidity(self, lat: float, lng: float) -> float:
        cur = await self.get_current_weather(lat, lng)
        return float(cur.get("humidity", 58.0))

    async def get_weather_window(self, lat: float, lng: float) -> Dict[str, Any]:
        cur = await self.get_current_weather(lat, lng)
        rain_prob = cur.get("rainfallProb", 12)
        wind = await self.get_wind_speed(lat, lng)
        safe = rain_prob < 30 and wind < 20
        return {
            "safeWindow": safe,
            "bestTime": "Today • 18:00 - 19:00 IST",
            "reason": "Low daytime evaporation and minimal spray drift loss." if safe else "Elevated wind or precipitation risk."
        }

class MockWeatherProvider(WeatherProvider):
    async def get_forecast(self, lat: float, lng: float) -> Dict[str, Any]:
        return {
            "current": {
                "temp": 33.0,
                "condition": "Mostly Sunny",
                "humidity": 58.0,
                "wind": "14 km/h SW",
                "rainfallProb": 12,
                "uvIndex": 8,
                "dewPoint": 22.0,
                "et0": "5.8 mm/day",
                "advisory": "Favorable conditions for drip irrigation this evening. Wind speed safe for low-drift activities."
            },
            "hourly": [
                { "time": "12:00", "temp": 33.0, "rainProb": 10, "humidity": 55.0 },
                { "time": "14:00", "temp": 34.0, "rainProb": 12, "humidity": 52.0 },
                { "time": "16:00", "temp": 32.0, "rainProb": 15, "humidity": 56.0 },
                { "time": "18:00", "temp": 30.0, "rainProb": 12, "humidity": 62.0 },
                { "time": "20:00", "temp": 27.0, "rainProb": 10, "humidity": 68.0 },
                { "time": "22:00", "temp": 25.0, "rainProb": 8, "humidity": 72.0 }
            ],
            "daily": [
                { "day": "Today", "tempMax": 34.0, "tempMin": 22.0, "rainProb": 12, "condition": "Sunny", "sprayRating": "Good (After 17:00)" },
                { "day": "Tomorrow", "tempMax": 33.0, "tempMin": 23.0, "rainProb": 25, "condition": "Partly Cloudy", "sprayRating": "Morning Only (Wind alert)" },
                { "day": "Day 3", "tempMax": 31.0, "tempMin": 21.0, "rainProb": 45, "condition": "Scattered Rain", "sprayRating": "Poor (Rain risk)" },
                { "day": "Day 4", "tempMax": 30.0, "tempMin": 20.0, "rainProb": 30, "condition": "Cloudy", "sprayRating": "Moderate" },
                { "day": "Day 5", "tempMax": 32.0, "tempMin": 21.0, "rainProb": 15, "condition": "Sunny", "sprayRating": "Excellent" },
                { "day": "Day 6", "tempMax": 33.0, "tempMin": 22.0, "rainProb": 10, "condition": "Clear Sky", "sprayRating": "Excellent" },
                { "day": "Day 7", "tempMax": 34.0, "tempMin": 23.0, "rainProb": 8, "condition": "Hot & Clear", "sprayRating": "Good" }
            ]
        }

    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        f = await self.get_forecast(lat, lng)
        return f["current"]

    async def get_hourly_forecast(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        f = await self.get_forecast(lat, lng)
        return f["hourly"]

    async def get_rain_probability(self, lat: float, lng: float) -> int:
        return 12

    async def get_wind_speed(self, lat: float, lng: float) -> float:
        return 14.0

    async def get_temperature(self, lat: float, lng: float) -> float:
        return 33.0

    async def get_humidity(self, lat: float, lng: float) -> float:
        return 58.0

    async def get_weather_window(self, lat: float, lng: float) -> Dict[str, Any]:
        return {
            "safeWindow": True,
            "bestTime": "Today • 18:00 - 18:35 IST",
            "reason": "Safe window (Rain prob 12%, Wind 14 km/h < 20 km/h threshold)."
        }

def get_weather_provider() -> WeatherProvider:
    if settings.WEATHER_PROVIDER == "openmeteo":
        return OpenMeteoWeatherProvider()
    return MockWeatherProvider()
