"""
Credit Card Expiration Date and CVV Generator

This module generates valid expiration dates and CVV codes for credit cards.
It complements the Luhn validator by providing complete credit card information.

Features:
- Generate future expiration dates
- Generate valid CVV codes based on card type
- Identify card type from card number
- Validate generated data
"""

import random
from datetime import datetime, timedelta
from typing import Tuple, Optional


class CardType:
    """Card type identifiers based on IIN (Issuer Identification Number)"""
    VISA = "Visa"
    MASTERCARD = "Mastercard"
    AMEX = "American Express"
    DISCOVER = "Discover"
    DINERS = "Diners Club"
    JCB = "JCB"
    UNKNOWN = "Unknown"


def identify_card_type(card_number: str) -> str:
    """
    Identify the card type based on the card number.
    
    Args:
        card_number: Credit card number (with or without spaces/hyphens)
    
    Returns:
        str: Card type (Visa, Mastercard, American Express, Discover, etc.)
    """
    # Remove spaces and hyphens
    cleaned = card_number.replace(" ", "").replace("-", "")
    
    if not cleaned.isdigit():
        return CardType.UNKNOWN
    
    # Get the first digit(s)
    first_digit = cleaned[0]
    first_two = cleaned[:2]
    first_four = cleaned[:4]
    
    # Visa: starts with 4
    if first_digit == '4':
        return CardType.VISA
    
    # Mastercard: starts with 51-55 or 2221-2720
    elif 51 <= int(first_two) <= 55:
        return CardType.MASTERCARD
    elif 2221 <= int(first_four) <= 2720:
        return CardType.MASTERCARD
    
    # American Express: starts with 34 or 37
    elif first_two in ['34', '37']:
        return CardType.AMEX
    
    # Discover: starts with 6011, 622126-622925, 644, 645, 646, 647, 648, 649, or 65
    elif first_four == '6011' or first_two == '65':
        return CardType.DISCOVER
    elif first_two in ['64', '65']:
        return CardType.DISCOVER
    
    # Diners Club: starts with 36, 38, or 39
    elif first_two in ['36', '38', '39']:
        return CardType.DINERS
    
    # JCB: starts with 3528-3589
    elif 3528 <= int(first_four) <= 3589:
        return CardType.JCB
    
    return CardType.UNKNOWN


def generate_expiration_date(min_months: int = 12, max_months: int = 120) -> str:
    """
    Generate a valid future expiration date.
    
    Args:
        min_months: Minimum months in the future (default: 12)
        max_months: Maximum months in the future (default: 120, i.e., 10 years)
    
    Returns:
        str: Expiration date in MM/YY format
    """
    # Generate random number of months between min and max
    months_ahead = random.randint(min_months, max_months)
    
    # Calculate future date
    today = datetime.now()
    future_date = today + timedelta(days=months_ahead * 30)  # Approximate conversion
    
    # Format as MM/YY
    month = str(future_date.month).zfill(2)
    year = str(future_date.year)[2:]  # Get last 2 digits
    
    return f"{month}/{year}"


def generate_cvv(card_type: str) -> str:
    """
    Generate a valid CVV code based on card type.
    
    CVV lengths:
    - Visa, Mastercard, Discover, JCB: 3 digits
    - American Express, Diners Club: 4 digits
    
    Args:
        card_type: Type of card (from identify_card_type)
    
    Returns:
        str: CVV code
    """
    if card_type == CardType.AMEX or card_type == CardType.DINERS:
        # 4-digit CVV for Amex and Diners
        return str(random.randint(1000, 9999))
    else:
        # 3-digit CVV for other cards
        return str(random.randint(100, 999))


def generate_card_credentials(card_number: str) -> dict:
    """
    Generate complete card credentials (expiration date and CVV).
    
    Args:
        card_number: Credit card number
    
    Returns:
        dict: Dictionary containing card info and generated credentials
    
    Raises:
        ValueError: If card number is invalid
    """
    # Remove spaces and hyphens
    cleaned = card_number.replace(" ", "").replace("-", "")
    
    # Validate card number format
    if not cleaned.isdigit():
        raise ValueError("Card number must contain only digits, spaces, or hyphens")
    
    if len(cleaned) < 13 or len(cleaned) > 19:
        raise ValueError("Card number must be between 13 and 19 digits")
    
    # Identify card type
    card_type = identify_card_type(cleaned)
    
    # Generate credentials
    expiration = generate_expiration_date()
    cvv = generate_cvv(card_type)
    
    return {
        "card_number": cleaned,
        "card_type": card_type,
        "expiration_date": expiration,
        "cvv": cvv,
        "formatted": {
            "card_number": f"{cleaned[:4]} {cleaned[4:8]} {cleaned[8:12]} {cleaned[12:]}",
            "expiration_date": expiration,
            "cvv": cvv
        }
    }


def validate_expiration_date(expiration: str) -> bool:
    """
    Validate that an expiration date is in the future.
    
    Args:
        expiration: Expiration date in MM/YY format
    
    Returns:
        bool: True if expiration date is in the future, False otherwise
    """
    try:
        month, year = expiration.split('/')
        month = int(month)
        year = int(year)
        
        # Convert 2-digit year to 4-digit year
        if year < 100:
            year += 2000
        
        # Create date for the last day of the expiration month
        if month == 12:
            expiry_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            expiry_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Check if expiration date is in the future
        return expiry_date > datetime.now()
    except (ValueError, IndexError):
        return False


if __name__ == "__main__":
    print("=== Credit Card Credential Generator ===\n")
    
    # Test card numbers
    test_cards = [
        "4532015112830366",      # Visa
        "5425233010103442",      # Mastercard
        "374245455400126",       # American Express
        "6011111111111117",      # Discover
    ]
    
    print("Generating credentials for test cards:\n")
    
    for card in test_cards:
        print(f"Card Number: {card}")
        
        try:
            credentials = generate_card_credentials(card)
            
            card_type = credentials["card_type"]
            formatted_card = credentials["formatted"]["card_number"]
            exp_date = credentials["expiration_date"]
            cvv = credentials["cvv"]
            
            print(f"Card Type: {card_type}")
            print(f"Formatted: {formatted_card}")
            print(f"Expiration: {exp_date}")
            print(f"CVV: {cvv}")
            print(f"Valid Expiration: {validate_expiration_date(exp_date)}")
            
        except ValueError as e:
            print(f"Error: {e}")
        
        print("-" * 50)
    
    print("\nGenerating multiple credentials for the same card:\n")
    card = "4532015112830366"
    print(f"Card: {card}\n")
    
    for i in range(3):
        print(f"Set {i + 1}:")
        credentials = generate_card_credentials(card)
        print(f"  Expiration: {credentials['expiration_date']}")
        print(f"  CVV: {credentials['cvv']}")
        print()
