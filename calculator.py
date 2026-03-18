"""Simple calculator module."""
import os
from typing import Union, List, Dict, Tuple, Optional
import requests


class Calculator:
    """Calculator class with history and chaining support."""
    
    def __init__(self) -> None:
        """Initialize calculator with empty history and last result."""
        self.last_result: float = 0.0
        self._history: List[Dict[str, Union[str, Tuple[float, float], float]]] = []
    
    def _validate_inputs(self, a: Union[float, int], b: Optional[Union[float, int]] = None) -> None:
        """Validate that inputs are numeric."""
        if not isinstance(a, (int, float)):
            raise TypeError(f"Expected numeric input, got {type(a).__name__}")
        if b is not None and not isinstance(b, (int, float)):
            raise TypeError(f"Expected numeric input, got {type(b).__name__}")
    
    def _record_operation(self, operation: str, args: Tuple[float, float], result: float) -> None:
        """Record operation in history with FIFO cap at 100."""
        self._history.append({
            "operation": operation,
            "args": args,
            "result": result
        })
        # Maintain FIFO cap at 100 items
        if len(self._history) > 100:
            self._history.pop(0)
    
    def add(self, a: Union[float, int], b: Optional[Union[float, int]] = None) -> float:
        """Add two numbers or chain with last result."""
        if b is None:
            self._validate_inputs(a)
            b = a
            a = self.last_result
        else:
            self._validate_inputs(a, b)
        
        result = float(a) + float(b)
        self.last_result = result
        self._record_operation("add", (float(a), float(b)), result)
        return result
    
    def subtract(self, a: Union[float, int], b: Optional[Union[float, int]] = None) -> float:
        """Subtract b from a or chain with last result."""
        if b is None:
            self._validate_inputs(a)
            b = a
            a = self.last_result
        else:
            self._validate_inputs(a, b)
        
        result = float(a) - float(b)
        self.last_result = result
        self._record_operation("subtract", (float(a), float(b)), result)
        return result
    
    def multiply(self, a: Union[float, int], b: Optional[Union[float, int]] = None) -> float:
        """Multiply two numbers or chain with last result."""
        if b is None:
            self._validate_inputs(a)
            b = a
            a = self.last_result
        else:
            self._validate_inputs(a, b)
        
        result = float(a) * float(b)
        self.last_result = result
        self._record_operation("multiply", (float(a), float(b)), result)
        return result
    
    def divide(self, a: Union[float, int], b: Optional[Union[float, int]] = None) -> float:
        """Divide a by b or chain with last result."""
        if b is None:
            self._validate_inputs(a)
            b = a
            a = self.last_result
        else:
            self._validate_inputs(a, b)
        
        if float(b) == 0:
            raise ValueError("Cannot divide by zero")
        
        result = float(a) / float(b)
        self.last_result = result
        self._record_operation("divide", (float(a), float(b)), result)
        return result
    
    @property
    def history(self) -> List[Dict[str, Union[str, Tuple[float, float], float]]]:
        """Return a copy of the operation history."""
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the operation history."""
        self._history.clear()


# Standalone functions for backwards compatibility
def add(a: float, b: float) -> float:
    """Add two numbers."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(b).__name__}")
    return float(a) + float(b)


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(b).__name__}")
    return float(a) - float(b)


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(b).__name__}")
    return float(a) * float(b)


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Expected numeric input, got {type(b).__name__}")
    if float(b) == 0:
        raise ValueError("Cannot divide by zero")
    return float(a) / float(b)


def get_weather(city: str) -> dict:
    """Fetch current weather data for a given city."""
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY environment variable is not set")
    
    try:
        response = requests.get(
            "https://api.weather.example.com/v1/current",
            params={"city": city, "key": api_key}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"Failed to fetch weather data for {city}: {str(e)}") from e
