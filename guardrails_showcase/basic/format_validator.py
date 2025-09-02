import re
from typing import Dict, Any, Optional
from guardrails.errors import ValidationError


def exact_format_validator(value: str, word_count: Optional[int] = None, 
                          all_caps: bool = False, pattern: Optional[str] = None,
                          allowed_chars: Optional[str] = None) -> str:
    """Validator function for exact format requirements"""
    value = value.strip()
    errors = []
    
    # Check word count
    if word_count:
        words = value.split()
        if len(words) != word_count:
            errors.append(f"Must contain exactly {word_count} words, found {len(words)}")
    
    # Check if all caps
    if all_caps:
        if not value.isupper():
            errors.append("All text must be in uppercase")
    
    # Check custom pattern
    if pattern:
        if not re.match(pattern, value):
            errors.append(f"Text must match pattern: {pattern}")
    
    # Check allowed characters
    if allowed_chars:
        invalid_chars = set(value) - set(allowed_chars)
        if invalid_chars:
            errors.append(f"Contains invalid characters: {', '.join(invalid_chars)}")
    
    if errors:
        raise ValidationError(f"Format validation failed: {'; '.join(errors)}")
    
    return value


class FormatGuard:
    """Simple guardrail for format validation"""
    
    def __init__(self, validator_type: str, **kwargs):
        self.validator_type = validator_type
        self.kwargs = kwargs
        
        # Set default configurations based on type
        if validator_type == 'two_words_caps':
            self.word_count = 2
            self.all_caps = True
            self.pattern = None
            self.allowed_chars = None
        elif validator_type == 'phone':
            self.word_count = None
            self.all_caps = False
            self.pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
            self.allowed_chars = None
        elif validator_type == 'email':
            self.word_count = None
            self.all_caps = False
            self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            self.allowed_chars = None
        elif validator_type == 'alphanumeric':
            self.word_count = None
            self.all_caps = False
            self.pattern = None
            allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            if kwargs.get('allow_spaces', False):
                allowed_chars += ' '
            self.allowed_chars = allowed_chars
        elif validator_type == 'custom':
            self.word_count = kwargs.get('word_count')
            self.all_caps = kwargs.get('all_caps', False)
            self.pattern = kwargs.get('pattern')
            self.allowed_chars = kwargs.get('allowed_chars')
        else:
            raise ValueError(f"Unknown validator type: {validator_type}")
    
    def validate(self, value: str) -> str:
        """Validate the input text"""
        return exact_format_validator(
            value, 
            word_count=self.word_count,
            all_caps=self.all_caps,
            pattern=self.pattern,
            allowed_chars=self.allowed_chars
        )


def create_format_guard(validator_type: str, **kwargs) -> FormatGuard:
    """Create a format validation guardrail"""
    return FormatGuard(validator_type, **kwargs)


def demo_format_validation():
    """Demo function to test format validation"""
    
    # Test two words, all caps
    guard_two_caps = create_format_guard('two_words_caps')
    
    test_inputs_caps = [
        "HELLO WORLD",
        "hello world",
        "HELLO WORLD EXTRA",
        "HELLO",
        "GOOD MORNING"
    ]
    
    results_caps = []
    for text in test_inputs_caps:
        try:
            validated = guard_two_caps.validate(text)
            results_caps.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results_caps.append({"input": text, "status": "FAILED", "reason": str(e)})
    
    # Test phone number format
    guard_phone = create_format_guard('phone')
    
    test_inputs_phone = [
        "(555) 123-4567",
        "555-123-4567",
        "5551234567", 
        "(555)123-4567",
        "(555) 123-456"
    ]
    
    results_phone = []
    for text in test_inputs_phone:
        try:
            validated = guard_phone.validate(text)
            results_phone.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results_phone.append({"input": text, "status": "FAILED", "reason": str(e)})
    
    # Test email format
    guard_email = create_format_guard('email')
    
    test_inputs_email = [
        "user@example.com",
        "test.email+tag@domain.co.uk", 
        "invalid-email",
        "user@",
        "@domain.com"
    ]
    
    results_email = []
    for text in test_inputs_email:
        try:
            validated = guard_email.validate(text)
            results_email.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results_email.append({"input": text, "status": "FAILED", "reason": str(e)})
    
    return {
        "two_words_caps": results_caps,
        "phone": results_phone,
        "email": results_email
    }