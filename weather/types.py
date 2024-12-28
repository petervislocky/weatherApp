from typing import TypedDict

class ConditionDict(TypedDict):
    text: str
    icon: str

class CurrentDict(TypedDict):
    temp_c: float
    temp_f: float
    feelslike_c: float
    feelslike_f: float
    wind_mph: float
    condition: ConditionDict

class LocationDict(TypedDict):
    name: str
    region: str

class WeatherDict(TypedDict):
    location: LocationDict
    current: CurrentDict