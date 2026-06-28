"""
Luhn Algorithm Credit Card Validator

The Luhn algorithm is a checksum formula used to validate credit card numbers
and detect simple errors in typing or transmission.

Algorithm steps:
1. From the rightmost digit (excluding the check digit), double every second digit
2. If the result of this doubling operation is greater than 9, subtract 9
3. Sum all the digits
4. If the total modulo 10 is equal to 0, the number is valid
"""


def is_valid_credit_card(card_number: str) -> bool:
    """
    Validate a credit card number using the Luhn algorithm.
    
    Args:
        card_number: Credit card number as a string (can contain spaces or hyphens)
    
    Returns:
        bool: True if the card number is valid, False otherwise
    
    Raises:
        ValueError: If the card number contains non-digit characters (excluding spaces/hyphens)
    """
    # Remove spaces and hyphens
    cleaned = card_number.replace(" ", "").replace("-", "")
    
    # Check if all characters are digits
    if not cleaned.isdigit():
        raise ValueError("Card number must contain only digits, spaces, or hyphens")
    
    # Card numbers should be between 13 and 19 digits
    if len(cleaned) < 13 or len(cleaned) > 19:
        raise ValueError("Card number must be between 13 and 19 digits")
    
    # Apply Luhn algorithm
    digits = [int(d) for d in cleaned]
    
    # Reverse the digits to process from right to left
    digits_reversed = digits[::-1]
    
    # Double every second digit (starting from index 1)
    for i in range(1, len(digits_reversed), 2):
        digits_reversed[i] *= 2
        # If doubled value > 9, subtract 9
        if digits_reversed[i] > 9:
            digits_reversed[i] -= 9
    
    # Sum all digits and check if divisible by 10
    total = sum(digits_reversed)
    return total % 10 == 0


def get_checksum_digit(partial_card: str) -> str:
    """
    Calculate the Luhn checksum digit for a partial credit card number.
    
    Args:
        partial_card: Partial credit card number (without check digit)
    
    Returns:
        str: The checksum digit (0-9)
    
    Raises:
        ValueError: If the input contains non-digit characters (excluding spaces/hyphens)
    """
    # Remove spaces and hyphens
    cleaned = partial_card.replace(" ", "").replace("-", "")
    
    # Check if all characters are digits
    if not cleaned.isdigit():
        raise ValueError("Card number must contain only digits, spaces, or hyphens")
    
    # Try each checksum digit (0-9) and find which one makes the number valid
    for check_digit in range(10):
        test_number = cleaned + str(check_digit)
        try:
            if is_valid_credit_card(test_number):
                return str(check_digit)
        except ValueError:
            continue
    
    return "0"  # Fallback (shouldn't reach here with valid input)


if __name__ == "__main__":
    # Example usage
    print("=== Luhn Algorithm Credit Card Validator ===\n")
    
    # Valid test card numbers
    test_cards = [
        "4532015112830366",  # Visa
        "5425233010103442",  # Mastercard
        "374245455400126",   # American Express
        "6011111111111117",  # Discover
        "4532-0151-1283-0366",  # Visa with hyphens
        "4532 0151 1283 0366",  # Visa with spaces
    ]
    
    print("Testing valid card numbers:")
    for card in test_cards:
        try:
            result = is_valid_credit_card(card)
            print(f"{card:20} -> Valid: {result}")
        except ValueError as e:
            print(f"{card:20} -> Error: {e}")
    
    print("\nTesting invalid card numbers:")
    invalid_cards = [
        "4532015112830367",  # Invalid checksum
        "1234567890123456",  # Invalid checksum
        "invalid",           # Non-numeric
        "12345",             # Too short
    ]
    
    for card in invalid_cards:
        try:
            result = is_valid_credit_card(card)
            print(f"{card:20} -> Valid: {result}")
        except ValueError as e:
            print(f"{card:20} -> Error: {e}")
    
    print("\nCalculating checksum digits:")
    partial_cards = [
        "453201511283036",
        "542523301010344",
        "37424545540012",
    ]
    
    for card in partial_cards:
        checksum = get_checksum_digit(card)
        full_card = card + checksum
        print(f"{card} + {checksum} = {full_card}")
