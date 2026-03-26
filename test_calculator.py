"""Tests for calculator module."""
import pytest
from unittest.mock import patch, Mock
from calculator import add, subtract, multiply, divide, Calculator, get_weather
import requests


# Backwards compatibility tests for standalone functions
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 5) == 0


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5


# Calculator class tests
def test_calculator_basic_operations():
    calc = Calculator()
    assert calc.add(5, 3) == 8
    assert calc.subtract(10, 4) == 6
    assert calc.multiply(3, 7) == 21
    assert calc.divide(15, 3) == 5.0


def test_calculator_chaining():
    calc = Calculator()
    # First operation sets last_result
    assert calc.add(5, 3) == 8
    assert calc.last_result == 8
    
    # Chain multiply: 8 * 2 = 16
    assert calc.multiply(2) == 16
    assert calc.last_result == 16
    
    # Chain subtract: 16 - 6 = 10
    assert calc.subtract(6) == 10
    assert calc.last_result == 10
    
    # Chain divide: 10 / 2 = 5
    assert calc.divide(2) == 5
    assert calc.last_result == 5


def test_calculator_history():
    calc = Calculator()
    
    # Perform operations
    calc.add(2, 3)
    calc.multiply(4, 5)
    calc.subtract(10, 3)
    
    # Check history
    history = calc.history
    assert len(history) == 3
    assert history[0] == {"operation": "add", "args": (2.0, 3.0), "result": 5.0}
    assert history[1] == {"operation": "multiply", "args": (4.0, 5.0), "result": 20.0}
    assert history[2] == {"operation": "subtract", "args": (10.0, 3.0), "result": 7.0}


def test_calculator_history_fifo_cap():
    calc = Calculator()
    
    # Add 105 operations to exceed the 100 item cap
    for i in range(105):
        calc.add(i, 1)
    
    # History should only have 100 items
    assert len(calc.history) == 100
    
    # First item should be from operation 5 (0-4 were removed)
    assert calc.history[0]["args"] == (5.0, 1.0)
    assert calc.history[-1]["args"] == (104.0, 1.0)


def test_calculator_clear_history():
    calc = Calculator()
    
    # Add some operations
    calc.add(1, 2)
    calc.multiply(3, 4)
    assert len(calc.history) == 2
    
    # Clear history
    calc.clear_history()
    assert len(calc.history) == 0
    
    # Last result should remain
    assert calc.last_result == 12.0


def test_calculator_initial_state():
    calc = Calculator()
    assert calc.last_result == 0.0
    assert len(calc.history) == 0


def test_calculator_type_errors():
    calc = Calculator()
    
    # Test with non-numeric inputs
    with pytest.raises(TypeError):
        calc.add("5", 3)
    
    with pytest.raises(TypeError):
        calc.add(5, "3")
    
    with pytest.raises(TypeError):
        calc.multiply(None, 5)
    
    with pytest.raises(TypeError):
        calc.subtract([1, 2], 3)
    
    # Test chaining with non-numeric
    calc.add(5, 5)  # Set last_result
    with pytest.raises(TypeError):
        calc.divide("2")


def test_standalone_functions_type_errors():
    # Test standalone functions also validate inputs
    with pytest.raises(TypeError):
        add("5", 3)
    
    with pytest.raises(TypeError):
        subtract(5, None)
    
    with pytest.raises(TypeError):
        multiply([], 5)
    
    with pytest.raises(TypeError):
        divide(10, "2")


def test_division_by_zero():
    calc = Calculator()
    
    # Test Calculator class
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)
    
    # Test chaining
    calc.add(10, 0)  # last_result = 10
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(0)
    
    # Test standalone function
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_calculator_float_conversion():
    calc = Calculator()
    
    # Test that integers are properly converted to floats
    result = calc.add(5, 3)
    assert isinstance(result, float)
    assert result == 8.0
    
    # Test in history
    assert calc.history[0]["result"] == 8.0
    assert calc.history[0]["args"] == (5.0, 3.0)


def test_history_immutability():
    calc = Calculator()
    calc.add(1, 2)
    
    # Get history and try to modify it
    history = calc.history
    history.append({"operation": "fake", "args": (0, 0), "result": 0})
    
    # Original history should be unchanged
    assert len(calc.history) == 1
    assert calc.history[0]["operation"] == "add"


def test_get_weather_success(monkeypatch):
    """Test successful weather fetch with mocked API response."""
    # Set the environment variable
    monkeypatch.setenv("WEATHER_API_KEY", "test-api-key")
    
    # Mock the requests.get call
    mock_response = Mock()
    mock_response.json.return_value = {
        "city": "New York",
        "temperature": 20,
        "conditions": "sunny"
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response) as mock_get:
        result = get_weather("New York")
        
        # Verify the API was called correctly
        mock_get.assert_called_once_with(
            "https://api.weather.example.com/v1/current",
            params={"city": "New York", "key": "test-api-key"}
        )
        
        # Verify the response
        assert result == {
            "city": "New York",
            "temperature": 20,
            "conditions": "sunny"
        }


def test_get_weather_http_error(monkeypatch):
    """Test HTTP error handling in get_weather."""
    # Set the environment variable
    monkeypatch.setenv("WEATHER_API_KEY", "test-api-key")
    
    # Mock the requests.get call to raise HTTPError
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            get_weather("InvalidCity")
        
        assert "Failed to fetch weather data for InvalidCity" in str(exc_info.value)


def test_get_weather_missing_api_key():
    """Test that ValueError is raised when WEATHER_API_KEY is not set."""
    # Don't set the environment variable (or ensure it's not set)
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            get_weather("New York")
        
        assert str(exc_info.value) == "WEATHER_API_KEY environment variable is not set"
