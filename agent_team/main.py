from google.adk.tools.tool_context import ToolContext
from google.adk.sessions import InMemorySessionService


def get_weather_stateful(
    city: str,
    tool_context: ToolContext
) -> dict:

    """
    Get weather based on the user's temperature preference.
    """

    weather_data = {
        "london": {
            "temp": 15,
            "condition": "Cloudy"
        },

        "new york": {
            "temp": 25,
            "condition": "Sunny"
        },

        "tokyo": {
            "temp": 18,
            "condition": "Rainy"
        }
    }

    city = city.lower().strip()

    if city not in weather_data:
        return {
            "status": "error",
            "message": "City not found."
        }

    # Read user preference from session state
    unit = tool_context.state.get(
        "temperature_unit",
        "Celsius"
    )

    data = weather_data[city]

    temperature = data["temp"]

    if unit == "Fahrenheit":
        temperature = (temperature * 9 / 5) + 32
        symbol = "°F"
    else:
        symbol = "°C"

    # Save last searched city
    tool_context.state["last_city"] = city

    return {
        "status": "success",
        "city": city,
        "temperature": f"{temperature:.1f}{symbol}",
        "condition": data["condition"]
    }

session_service = InMemorySessionService()

APP_NAME = "weather_app"
USER_ID = "user_001"
SESSION_ID = "session_001"

async def create_app_session():

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,

        state={
            "temperature_unit": "Celsius"
        }
    )

    return session