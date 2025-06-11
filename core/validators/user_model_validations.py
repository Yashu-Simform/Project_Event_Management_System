from string import punctuation
import re

def validate_password(value: str):
    """
        Validates password: 
        Conditions it checks:
            -   Min length 8
            -   Max length 64
            -   At least 1 uppercase
            -   At least 1 lowercase
            -   At least 1 digit
            -   At least 1 special character
    """

    if not value:
        raise ValueError('Invalid Password! Password cannot be None.')

    if len(value) < 8:
        raise ValueError('Invalid Password! Password must contains at least 8 characters.')
    
    if len(value) > 64:
        raise ValueError('Invalid Password! Password must contains at max 64 characters.')
    
    has_lowercase = re.search(r'[a-z]', value)
    has_uppercase = re.search(r'[A-Z]', value)
    has_digit = re.search(r'\d', value)
    has_special_char = re.search(rf'[{punctuation}]', value)

    if not (has_lowercase and has_uppercase and has_digit and has_special_char):
        raise ValueError('Invalid Password! Password must contain at least 1 lowercase, 1 uppercase, 1 digit and 1 special character.')
    
    return value
