"""Stripe payment processing module."""
import requests


STRIPE_SECRET_KEY = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


class PaymentError(Exception):
    """Exception raised for payment processing errors."""
    pass


def process_payment(amount: float, currency: str) -> dict:
    """Process a payment through Stripe API."""
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Expected numeric amount, got {type(amount).__name__}")
    if not isinstance(currency, str):
        raise TypeError(f"Expected string currency, got {type(currency).__name__}")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if not currency:
        raise ValueError("Currency must be a non-empty string")
    
    try:
        response = requests.post(
            "https://api.stripe.com/v1/charges",
            auth=(STRIPE_SECRET_KEY, ''),
            data={"amount": amount, "currency": currency}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise PaymentError(f"Payment processing failed: {str(e)}") from e