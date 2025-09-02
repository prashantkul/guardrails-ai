"""
TUTORIAL 2: Valid JSON Guardrail
=================================

OBJECTIVE: Create a guardrail that ensures AI outputs are valid JSON format.

LEARNING GOALS:
- Understand JSON validation
- Handle parsing errors gracefully
- Implement schema validation (optional)
- Fix common JSON formatting issues

DIFFICULTY: ⭐⭐☆ (Intermediate)
"""

import json
import re
from typing import Dict, Any, Optional
from guardrails.errors import ValidationError


class ValidJSONGuard:
    """
    A guardrail that validates and ensures content is valid JSON.
    
    TODO: Students will implement JSON validation and optional fixing logic.
    """
    
    def __init__(self, fix_common_errors: bool = True, required_keys: Optional[list] = None,
                 strict_mode: bool = False):
        """
        Initialize the JSON validation guardrail.
        
        Args:
            fix_common_errors: Whether to attempt fixing common JSON formatting errors
            required_keys: List of keys that must be present in the JSON object
            strict_mode: If True, be strict about JSON formatting (no automatic fixes)
        """
        self.fix_common_errors = fix_common_errors
        self.required_keys = required_keys or []
        self.strict_mode = strict_mode
    
    def validate(self, value: str) -> str:
        """
        Validate and potentially fix JSON content.
        
        Args:
            value: Input text to validate as JSON
            
        Returns:
            str: Valid JSON string (potentially fixed)
            
        Raises:
            ValidationError: If JSON is invalid and can't be fixed
        """
        if not value or not isinstance(value, str):
            raise ValidationError("Input must be a non-empty string")
        
        # TODO: STUDENT TASK 1
        # Try to parse the JSON as-is first
        # YOUR CODE HERE:
        try:
            parsed_data = json.loads(value.strip())
            # TODO: If parsing succeeds, validate the structure
            # Call self._validate_structure(parsed_data)
            # Return the original value if valid
            pass
        except json.JSONDecodeError as e:
            # TODO: If parsing fails and fix_common_errors is True, try to fix
            if self.fix_common_errors and not self.strict_mode:
                # TODO: Call self._attempt_json_fix(value)
                pass
            else:
                # TODO: Raise ValidationError with the JSON parsing error
                pass
    
    def _validate_structure(self, data: Any) -> None:
        """
        Validate the structure of parsed JSON data.
        
        TODO: STUDENT TASK 2
        # Check if required keys are present (if data is a dict)
        # YOUR CODE HERE:
        """
        if isinstance(data, dict) and self.required_keys:
            missing_keys = []
            for key in self.required_keys:
                # TODO: Check if key is in data, add to missing_keys if not
                pass
            
            if missing_keys:
                # TODO: Raise ValidationError listing missing keys
                pass
    
    def _attempt_json_fix(self, value: str) -> str:
        """
        Attempt to fix common JSON formatting errors.
        
        TODO: STUDENT TASK 3
        # Implement common JSON fixes:
        # 1. Fix single quotes to double quotes
        # 2. Fix trailing commas
        # 3. Fix unquoted keys
        # 4. Handle basic escaping issues
        # YOUR CODE HERE:
        """
        fixed_value = value.strip()
        
        # TODO: Fix 1 - Replace single quotes with double quotes (be careful with apostrophes)
        # HINT: This is tricky! Consider using regex to match quote pairs
        
        # TODO: Fix 2 - Remove trailing commas before closing braces/brackets
        # HINT: Use regex to find patterns like ",}" or ",]"
        
        # TODO: Fix 3 - Quote unquoted keys in objects
        # HINT: Look for patterns like {key: value} and convert to {"key": value}
        
        # TODO: Fix 4 - Try parsing the fixed JSON
        try:
            parsed_data = json.loads(fixed_value)
            self._validate_structure(parsed_data)
            # TODO: Return properly formatted JSON
            pass
        except json.JSONDecodeError as e:
            # TODO: If still invalid, raise ValidationError
            pass
    
    def _fix_single_quotes(self, text: str) -> str:
        """
        Helper method to fix single quotes in JSON.
        
        TODO: STUDENT TASK 4 (ADVANCED)
        # This is challenging! Need to distinguish between:
        # - String delimiters: 'hello' -> "hello"  
        # - Apostrophes inside strings: "don't" (should stay as is)
        # 
        # For now, implement a simple version:
        # Replace single quotes with double quotes, but be careful!
        # YOUR CODE HERE:
        """
        # Simple approach: replace single quotes that are likely string delimiters
        # This is not perfect but works for many cases
        return text.replace("'", '"')
    
    def _remove_trailing_commas(self, text: str) -> str:
        """
        Helper method to remove trailing commas.
        
        TODO: STUDENT TASK 5
        # Remove commas that appear before closing braces or brackets
        # YOUR CODE HERE:
        """
        # TODO: Use regex to find and remove patterns like ",}" and ",]"
        # HINT: Use re.sub() with appropriate patterns
        pass


def create_json_guard(**kwargs) -> ValidJSONGuard:
    """Factory function to create a JSON validation guard."""
    return ValidJSONGuard(**kwargs)


# Test scenarios for students to validate their implementation
def test_valid_json():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Valid JSON Guardrail")
    print("=" * 50)
    
    # Test case 1: Basic JSON validation
    basic_guard = create_json_guard(fix_common_errors=False, strict_mode=True)
    
    test_cases_1 = [
        ('{"name": "John", "age": 30}', "SHOULD_PASS"),
        ('[1, 2, 3, 4, 5]', "SHOULD_PASS"),
        ('{"valid": true, "number": 42}', "SHOULD_PASS"),
        ('{"name": "John", "age": 30,}', "SHOULD_FAIL"),  # Trailing comma
        ("{'name': 'John', 'age': 30}", "SHOULD_FAIL"),  # Single quotes
        ('{name: "John", age: 30}', "SHOULD_FAIL"),  # Unquoted keys
        ('Invalid JSON content', "SHOULD_FAIL"),
    ]
    
    print("\n📝 Test 1: Basic JSON Validation (Strict Mode)")
    _run_json_test_cases(basic_guard, test_cases_1)
    
    # Test case 2: JSON with automatic fixing
    fixing_guard = create_json_guard(fix_common_errors=True, strict_mode=False)
    
    test_cases_2 = [
        ('{"name": "John", "age": 30}', "SHOULD_PASS"),
        ('{"name": "John", "age": 30,}', "SHOULD_PASS"),  # Should fix trailing comma
        ("{'name': 'John', 'age': 30}", "SHOULD_PASS"),  # Should fix single quotes
        ('{name: "John", age: 30}', "SHOULD_PASS"),  # Should fix unquoted keys (advanced)
        ('Completely invalid content', "SHOULD_FAIL"),  # Can't be fixed
    ]
    
    print("\n📝 Test 2: JSON with Automatic Fixing")
    _run_json_test_cases(fixing_guard, test_cases_2)
    
    # Test case 3: Required keys validation
    required_keys_guard = create_json_guard(
        fix_common_errors=True,
        required_keys=["name", "email"]
    )
    
    test_cases_3 = [
        ('{"name": "John", "email": "john@example.com"}', "SHOULD_PASS"),
        ('{"name": "John", "email": "john@example.com", "age": 30}', "SHOULD_PASS"),
        ('{"name": "John"}', "SHOULD_FAIL"),  # Missing email
        ('{"email": "john@example.com"}', "SHOULD_FAIL"),  # Missing name
        ('[]', "SHOULD_FAIL"),  # Not an object
    ]
    
    print("\n📝 Test 3: Required Keys Validation")
    _run_json_test_cases(required_keys_guard, test_cases_3)


def _run_json_test_cases(guard: ValidJSONGuard, test_cases: list):
    """Helper function to run JSON test cases."""
    for i, (json_text, expected) in enumerate(test_cases, 1):
        try:
            result = guard.validate(json_text)
            if result is None:
                # Handle case where TODO is not implemented
                status = "⚠️  NOT IMPLEMENTED" if expected == "SHOULD_PASS" else "⚠️  NOT IMPLEMENTED"
                print(f"{i}. '{json_text[:40]}...' → {status}")
                print("   Note: Complete the TODO sections to run this test")
                continue
            status = "✅ PASSED" if expected == "SHOULD_PASS" else "❌ UNEXPECTED PASS"
            print(f"{i}. '{json_text[:40]}...' → {status}")
            if expected == "SHOULD_PASS" and result:
                # Show the (potentially fixed) result
                try:
                    formatted = json.dumps(json.loads(result), indent=2)
                    print(f"   Result: {formatted[:100]}...")
                except:
                    if result:
                        print(f"   Result: {result[:60]}...")
        except ValidationError as e:
            status = "✅ BLOCKED" if expected == "SHOULD_FAIL" else "❌ UNEXPECTED BLOCK"
            print(f"{i}. '{json_text[:40]}...' → {status}")
            if expected == "SHOULD_FAIL":
                print(f"   Reason: {e}")


if __name__ == "__main__":
    """
    STUDENT INSTRUCTIONS:
    ====================
    
    1. Complete the TODO sections in the ValidJSONGuard class
    2. Start with the basic validation (Task 1 and 2)
    3. Then implement the JSON fixing logic (Tasks 3-5)
    4. Run this file to test: python 02_valid_json.py
    5. All tests should pass with appropriate PASS/BLOCK results
    
    HINTS:
    ------
    - Use json.loads() to parse JSON and catch JSONDecodeError
    - For fixing trailing commas: use re.sub(r',(\\s*[}\\]])', r'\\1', text)
    - For single quotes: be careful about apostrophes! Simple replace works for basic cases
    - For unquoted keys: use regex to find {key: value} patterns
    - Always re-validate after fixing
    
    COMMON JSON ERRORS TO FIX:
    --------------------------
    1. Trailing commas: {"a": 1,} → {"a": 1}
    2. Single quotes: {'a': 'b'} → {"a": "b"}
    3. Unquoted keys: {a: "b"} → {"a": "b"}
    4. Missing quotes around strings
    
    EXTENSION CHALLENGES:
    --------------------
    - Add support for JSON schema validation
    - Handle more complex quote fixing (nested quotes, escaped quotes)
    - Add support for JSON comments removal
    - Implement pretty-printing options
    - Add support for JSONL (JSON Lines) format
    """
    test_valid_json()