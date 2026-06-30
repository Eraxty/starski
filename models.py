from dataclasses import dataclass

@dataclass
class obj:
    name: str
    altitude: float
    azimuth: float
    symbol: str
    magnitude: float = 0.0