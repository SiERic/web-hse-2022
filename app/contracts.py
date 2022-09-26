from pydantic import BaseModel

from enum import Enum


class Color(str, Enum):
    """Frog color"""
    GREEN = "GREEN"
    RED = "RED"
    BLUE = "BLUE"


class Frog(BaseModel):
    """Contract for frog"""
    name: str
    color: Color
