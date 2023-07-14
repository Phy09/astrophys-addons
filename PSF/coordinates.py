from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Coordinates:
    x: float
    y: float