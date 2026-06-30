from dataclasses import dataclass

@dataclass
class obj:
    name: str
    altitude: float
    azimuth: float
    magnitude: float = 0.0
    type: str = "star"  