"""Tests for payment processing module."""
import pytest
from unittest.mock import patch, Mock
import requests
from payments import process_payment, PaymentError, STRIPE_SECRET_KEY


def test_process_payment_success():
    """Test successful payment processing."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": "ch_1ABC123",
        "amount": 1000,
        "currency": "usd",
        "status": "succeeded"
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.post", return_value=mock_response) as mock_post:
        result = process_payment(1000, "usd")
        
        mock_post.assert_called_once_with(
            "https://api.stripe.com/v1/charges",
            auth=(STRIPE_SECRET_KEY, ''),
            data={"amount": 1000, "currency": "usd"}
        )
        
        assert result == {
            "id": "ch_1ABC123",
            "amount": 1000,
            "currency": "usd",
            "status": "succeeded"
        }


def test_process_payment_http_error():
    """Test payment processing with HTTP error."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("402 Payment Required")
    
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(PaymentError) as exc_info:
            process_payment(500, "eur")
        
        assert "Payment processing failed" in str(exc_info.value)


def test_process_payment_invalid_amount():
    """Test payment processing with invalid amount values."""
    # Zero amount
    with pytest.raises(ValueError) as exc_info:
        process_payment(0, "usd")
    assert "Amount must be positive" in str(exc_info.value)
    
    # Negative amount
    with pytest.raises(ValueError) as exc_info:
        process_payment(-100, "usd")
    assert "Amount must be positive" in str(exc_info.value)
    
    # Non-numeric amount
    with pytest.raises(TypeError) as exc_info:
        process_payment("1000", "usd")
    assert "Expected numeric amount" in str(exc_info.value)
    
    # None as amount
    with pytest.raises(TypeError) as exc_info:
        process_payment(None, "usd")
    assert "Expected numeric amount" in str(exc_info.value)


def test_process_payment_invalid_currency():
    """Test payment processing with invalid currency values."""
    # Empty currency
    with pytest.raises(ValueError) as exc_info:
        process_payment(1000, "")
    assert "Currency must be a non-empty string" in str(exc_info.value)
    
    # Non-string currency
    with pytest.raises(TypeError) as exc_info:
        process_payment(1000, 123)
    assert "Expected string currency" in str(exc_info.value)
    
    # None as currency
    with pytest.raises(TypeError) as exc_info:
        process_payment(1000, None)
    assert "Expected string currency" in str(exc_info.value)


def test_process_payment_float_amount():
    """Test payment processing with float amount."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": "ch_2DEF456",
        "amount": 99.99,
        "currency": "gbp",
        "status": "succeeded"
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.post", return_value=mock_response) as mock_post:
        result = process_payment(99.99, "gbp")
        
        mock_post.assert_called_once_with(
            "https://api.stripe.com/v1/charges",
            auth=(STRIPE_SECRET_KEY, ''),
            data={"amount": 99.99, "currency": "gbp"}
        )
        
        assert result["amount"] == 99.99