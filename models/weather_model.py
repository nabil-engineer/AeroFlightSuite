class Weather:
    def __init__(
        self,
        temperature,
        wind_speed,
        wind_direction,
        pressure,
        humidity,
        visibility,
        condition,
        severity,
    ):
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.pressure = pressure
        self.humidity = humidity
        self.visibility = visibility
        self.condition = condition
        self.severity = severity

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "pressure": self.pressure,
            "humidity": self.humidity,
            "visibility": self.visibility,
            "condition": self.condition,
            "severity": self.severity,
        }