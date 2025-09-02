"""
TUTORIAL 1: Ban List Guardrail
===============================

OBJECTIVE: Create a guardrail that prevents content containing banned words/phrases.

LEARNING GOALS:
- Understand basic pattern matching
- Implement case-insensitive filtering
- Handle partial word matches
- Create flexible ban lists

DIFFICULTY: ⭐☆☆ (Beginner)
"""

import re
from typing import List, Set
from guardrails.errors import ValidationError


class BanListGuard:
    """
    A guardrail that blocks content containing banned words or phrases.
    
    TODO: Students will implement the core validation logic.
    """
    
    def __init__(self, banned_items: List[str], case_sensitive: bool = False, 
                 partial_match: bool = True):
        """
        Initialize the ban list guardrail.
        
        Args:
            banned_items: List of words/phrases to ban
            case_sensitive: Whether matching should be case sensitive
            partial_match: Whether to match partial words (e.g., "spam" in "spammer")
        """
        self.banned_items = banned_items
        self.case_sensitive = case_sensitive
        self.partial_match = partial_match
        
        # TODO: STUDENT TASK 1
        # Convert banned_items to appropriate format based on case_sensitive setting
        # HINT: Consider using set() for faster lookups
        # YOUR CODE HERE:
        if case_sensitive:
            self.banned_set = set(banned_items)
        else:
            # TODO: Convert all items to lowercase for case-insensitive matching
            pass
    
    def validate(self, value: str) -> str:
        """
        Validate input text against the ban list.
        
        Args:
            value: Input text to validate
            
        Returns:
            str: Original value if valid
            
        Raises:
            ValidationError: If banned content is detected
        """
        if not value or not isinstance(value, str):
            return value
            
        # TODO: STUDENT TASK 2
        # Implement the main validation logic
        # YOUR CODE HERE:
        
        text_to_check = value if self.case_sensitive else value.lower()
        
        for banned_item in self.banned_set:
            if self.partial_match:
                # TODO: Check if banned_item appears anywhere in text_to_check
                # HINT: Use 'in' operator or regex
                pass
            else:
                # TODO: Check for exact word matches only
                # HINT: Use word boundaries with regex or split by spaces
                pass
        
        # If no banned content found, return original value
        return value
    
    def _is_whole_word_match(self, text: str, banned_word: str) -> bool:
        """
        Helper method to check for whole word matches.
        
        TODO: STUDENT TASK 3
        # Implement whole word matching using regex word boundaries
        # HINT: Use r'\b' for word boundaries
        # YOUR CODE HERE:
        """
        pass


def create_ban_list_guard(banned_items: List[str], **kwargs) -> BanListGuard:
    """Factory function to create a ban list guard."""
    return BanListGuard(banned_items, **kwargs)


# Test scenarios for students to validate their implementation
def test_ban_list():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Ban List Guardrail")
    print("=" * 50)
    
    # Test case 1: Basic profanity filter
    profanity_guard = create_ban_list_guard(
        banned_items=["spam", "scam", "fake", "virus"],
        case_sensitive=False,
        partial_match=True
    )
    
    test_cases_1 = [
        ("This is a great product!", "SHOULD_PASS"),
        ("This is spam content", "SHOULD_FAIL"),  
        ("Don't fall for this SCAM", "SHOULD_FAIL"),
        ("Fake news everywhere", "SHOULD_FAIL"),
        ("Download this virus", "SHOULD_FAIL"),
        ("I love spam and eggs", "SHOULD_FAIL"),  # Should catch "spam"
    ]
    
    print("\n📝 Test 1: Basic Profanity Filter")
    _run_test_cases(profanity_guard, test_cases_1)
    
    # Test case 2: Whole word matching
    whole_word_guard = create_ban_list_guard(
        banned_items=["cat", "dog"],
        case_sensitive=False,
        partial_match=False
    )
    
    test_cases_2 = [
        ("I have a cat", "SHOULD_FAIL"),
        ("The dog is cute", "SHOULD_FAIL"), 
        ("Education is important", "SHOULD_PASS"),  # "cat" in "education" should pass
        ("Catalog of items", "SHOULD_PASS"),  # "cat" in "catalog" should pass
        ("CAT in caps", "SHOULD_FAIL"),
    ]
    
    print("\n📝 Test 2: Whole Word Matching")
    _run_test_cases(whole_word_guard, test_cases_2)
    
    # Test case 3: Case sensitive matching
    case_sensitive_guard = create_ban_list_guard(
        banned_items=["SECRET", "API"],
        case_sensitive=True,
        partial_match=True
    )
    
    test_cases_3 = [
        ("This is a SECRET document", "SHOULD_FAIL"),
        ("This is a secret document", "SHOULD_PASS"),  # Different case
        ("API key exposed", "SHOULD_FAIL"),
        ("api key exposed", "SHOULD_PASS"),  # Different case
    ]
    
    print("\n📝 Test 3: Case Sensitive Matching")
    _run_test_cases(case_sensitive_guard, test_cases_3)


def _run_test_cases(guard: BanListGuard, test_cases: List[tuple]):
    """Helper function to run test cases."""
    for i, (text, expected) in enumerate(test_cases, 1):
        try:
            result = guard.validate(text)
            status = "✅ PASSED" if expected == "SHOULD_PASS" else "❌ UNEXPECTED PASS"
            print(f"{i}. '{text[:50]}...' → {status}")
        except ValidationError as e:
            status = "✅ BLOCKED" if expected == "SHOULD_FAIL" else "❌ UNEXPECTED BLOCK"
            print(f"{i}. '{text[:50]}...' → {status}")
            if expected == "SHOULD_FAIL":
                print(f"   Reason: {e}")


if __name__ == "__main__":
    """
    STUDENT INSTRUCTIONS:
    ====================
    
    1. Complete the TODO sections in the BanListGuard class
    2. Run this file to test your implementation: python 01_ban_list.py
    3. All tests should pass with appropriate PASS/BLOCK results
    4. Experiment with different banned_items lists
    
    HINTS:
    ------
    - Use set() for O(1) lookup performance
    - For case-insensitive matching, convert everything to lowercase
    - For partial matching, use 'in' operator: if banned in text
    - For whole word matching, use regex with word boundaries: r'\\b' + word + r'\\b'
    - Remember to raise ValidationError with descriptive message when banned content is found
    
    EXTENSION CHALLENGES:
    --------------------
    - Add support for regex patterns in ban list
    - Implement whitelist exceptions (words that should be allowed even if they contain banned substrings)
    - Add severity levels (warning vs blocking)
    - Create ban lists for different categories (profanity, spam, phishing, etc.)
    """
    test_ban_list()