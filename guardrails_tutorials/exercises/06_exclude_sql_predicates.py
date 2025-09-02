"""
TUTORIAL 6: Exclude SQL Predicates Guardrail
=============================================

OBJECTIVE: Create a guardrail that prevents SQL injection attempts and malicious SQL predicates.

LEARNING GOALS:
- Understand SQL injection patterns and risks
- Implement SQL predicate detection
- Handle various SQL injection techniques
- Create safe SQL filtering mechanisms

DIFFICULTY: ⭐⭐☆ (Intermediate)
"""

import re
from typing import List, Set, Dict, Tuple
from guardrails.errors import ValidationError


class ExcludeSQLPredicatesGuard:
    """
    A guardrail that detects and blocks SQL injection attempts and malicious predicates.
    
    TODO: Students will implement SQL injection detection methods.
    """
    
    def __init__(self, strict_mode: bool = False, 
                 allow_basic_queries: bool = False,
                 blocked_keywords: List[str] = None):
        """
        Initialize the SQL predicates exclusion guardrail.
        
        Args:
            strict_mode: If True, block any SQL-like syntax
            allow_basic_queries: If True, allow safe SELECT queries
            blocked_keywords: Additional SQL keywords to block
        """
        self.strict_mode = strict_mode
        self.allow_basic_queries = allow_basic_queries
        self.blocked_keywords = set((blocked_keywords or []))
        
        # Common SQL injection patterns
        self.sql_injection_patterns = [
            # Classic injection patterns
            r"'\s*;\s*",  # End statement and start new
            r"'\s*\|\|\s*",  # SQL concatenation
            r"'\s*\+\s*",  # SQL string concatenation
            r"--\s*",  # SQL comments
            r"/\*.*?\*/",  # Multi-line comments
            r"'\s*and\s+'.*?'='",  # Always true conditions
            r"'\s*or\s+'.*?'='",  # Always true conditions
            r"1\s*=\s*1",  # Always true
            r"1\s*or\s*1",  # Always true
            
            # Union-based injection
            r"\bunion\s+select\b",
            r"\bunion\s+all\s+select\b",
            
            # Boolean-based injection
            r"'\s*and\s+\d+\s*=\s*\d+",
            r"'\s*or\s+\d+\s*=\s*\d+",
            
            # Time-based injection
            r"\bwaitfor\s+delay\b",
            r"\bsleep\s*\(",
            r"\bbenchmark\s*\(",
            
            # Error-based injection
            r"\bcast\s*\(",
            r"\bconvert\s*\(",
            r"\bextractvalue\s*\(",
        ]
        
        # Dangerous SQL keywords
        self.dangerous_keywords = {
            'drop', 'delete', 'truncate', 'alter', 'create', 'insert', 'update',
            'exec', 'execute', 'sp_executesql', 'xp_cmdshell', 'sp_configure',
            'union', 'having', 'group_concat', 'load_file', 'into outfile'
        }
        
        # Add custom blocked keywords
        self.dangerous_keywords.update(self.blocked_keywords)
    
    def validate(self, value: str) -> str:
        """
        Validate content for SQL injection attempts.
        
        Args:
            value: Input text to validate
            
        Returns:
            str: Original value if no SQL threats detected
            
        Raises:
            ValidationError: If SQL injection patterns are found
        """
        if not value or not isinstance(value, str):
            return value
        
        issues = []
        
        # TODO: STUDENT TASK 1
        # Check for SQL injection patterns
        # Call self._detect_injection_patterns(value)
        pattern_issues = []  # TODO: Implement this
        
        # TODO: STUDENT TASK 2
        # Check for dangerous SQL keywords
        # Call self._detect_dangerous_keywords(value)
        keyword_issues = []  # TODO: Implement this
        
        # TODO: STUDENT TASK 3
        # Check for SQL predicates and logical operators
        # Call self._detect_sql_predicates(value)
        predicate_issues = []  # TODO: Implement this
        
        # TODO: STUDENT TASK 4
        # In strict mode, check for any SQL-like syntax
        if self.strict_mode:
            # TODO: Call self._detect_sql_syntax(value)
            syntax_issues = []  # TODO: Implement this
        
        # TODO: Combine all issues and raise error if any found
        all_issues = pattern_issues + keyword_issues + predicate_issues
        if self.strict_mode:
            all_issues.extend(syntax_issues)
        
        if all_issues:
            # TODO: Raise ValidationError with combined issues
            pass
        
        return value
    
    def _detect_injection_patterns(self, text: str) -> List[str]:
        """
        Detect common SQL injection patterns.
        
        TODO: STUDENT TASK 5
        # Use self.sql_injection_patterns to find injection attempts
        # YOUR CODE HERE:
        """
        issues = []
        text_lower = text.lower()
        
        for pattern in self.sql_injection_patterns:
            # TODO: Use re.search to find pattern matches
            # If found, add appropriate description to issues
            pass
        
        return issues
    
    def _detect_dangerous_keywords(self, text: str) -> List[str]:
        """
        Detect dangerous SQL keywords.
        
        TODO: STUDENT TASK 6
        # Look for dangerous SQL keywords in the text
        # YOUR CODE HERE:
        """
        issues = []
        text_lower = text.lower()
        
        # TODO: Split text into words
        words = []  # TODO: Extract words from text
        
        found_keywords = []
        for word in words:
            # TODO: Check if word is in self.dangerous_keywords
            # If found, add to found_keywords list
            pass
        
        if found_keywords:
            # TODO: Add issue describing found dangerous keywords
            pass
        
        return issues
    
    def _detect_sql_predicates(self, text: str) -> List[str]:
        """
        Detect SQL predicates and logical operators that might be injection attempts.
        
        TODO: STUDENT TASK 7
        # Look for SQL predicates like WHERE clauses, AND/OR operations, etc.
        # YOUR CODE HERE:
        """
        issues = []
        text_lower = text.lower()
        
        # Common SQL predicate patterns
        predicate_patterns = [
            r"\bwhere\s+.*?=",  # WHERE clauses
            r"\band\s+.*?=",    # AND conditions
            r"\bor\s+.*?=",     # OR conditions
            r"=\s*'.*?'",       # String comparisons
            r"\blike\s+'.*?%",  # LIKE patterns
            r"\bin\s*\(",       # IN clauses
            r"\bexists\s*\(",   # EXISTS clauses
        ]
        
        # TODO: Check each predicate pattern
        for pattern in predicate_patterns:
            # TODO: Use re.search to find matches
            # Consider context - are these legitimate or suspicious?
            pass
        
        return issues
    
    def _detect_sql_syntax(self, text: str) -> List[str]:
        """
        Detect any SQL-like syntax (for strict mode).
        
        TODO: STUDENT TASK 8
        # In strict mode, detect any SQL-like syntax
        # YOUR CODE HERE:
        """
        issues = []
        text_lower = text.lower()
        
        # SQL syntax indicators
        sql_syntax_patterns = [
            r"\bselect\b",
            r"\bfrom\b",
            r"\bwhere\b",
            r"\border\s+by\b",
            r"\bgroup\s+by\b",
            r"\bhaving\b",
            r"\bjoin\b",
            r"\bleft\s+join\b",
            r"\bright\s+join\b",
            r"\binner\s+join\b",
        ]
        
        found_syntax = []
        for pattern in sql_syntax_patterns:
            # TODO: Check if pattern exists in text
            # If allow_basic_queries is True, be more lenient with SELECT
            pass
        
        if found_syntax:
            # TODO: Add issue about SQL syntax detection
            pass
        
        return issues
    
    def _extract_words(self, text: str) -> List[str]:
        """
        Extract words from text for keyword analysis.
        
        TODO: STUDENT TASK 9
        # Extract words and convert to lowercase
        # YOUR CODE HERE:
        """
        # TODO: Use regex to extract words
        # TODO: Convert to lowercase
        # TODO: Filter out very short words
        words = []
        return words
    
    def _is_likely_injection(self, text: str) -> bool:
        """
        Determine if text is likely a SQL injection attempt.
        
        TODO: STUDENT TASK 10 (ADVANCED)
        # Use heuristics to determine if text looks like SQL injection
        # Consider: quote patterns, keyword density, suspicious combinations
        # YOUR CODE HERE:
        """
        text_lower = text.lower()
        
        # Heuristic scoring
        injection_score = 0
        
        # TODO: Count suspicious patterns
        quote_count = text.count("'")
        if quote_count > 2:
            injection_score += 1
        
        # TODO: Check for suspicious keyword combinations
        suspicious_combinations = [
            ("'", "or", "="),
            ("'", "and", "="),
            ("union", "select"),
            ("'", ";", "--"),
        ]
        
        # TODO: Score based on combinations found
        
        return injection_score >= 2


def create_sql_guard(**kwargs) -> ExcludeSQLPredicatesGuard:
    """Factory function to create a SQL predicates guard."""
    return ExcludeSQLPredicatesGuard(**kwargs)


# Test scenarios for students to validate their implementation
def test_exclude_sql_predicates():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Exclude SQL Predicates Guardrail")
    print("=" * 50)
    
    # Test case 1: Basic SQL injection detection
    basic_guard = create_sql_guard(strict_mode=False, allow_basic_queries=False)
    
    test_cases_1 = [
        ("Hello, how are you today?", "SHOULD_PASS"),
        ("The user ID is 123 and the status is active.", "SHOULD_PASS"),
        ("'; DROP TABLE users; --", "SHOULD_FAIL"),
        ("' OR '1'='1", "SHOULD_FAIL"),
        ("admin'--", "SHOULD_FAIL"),
        ("' UNION SELECT * FROM passwords --", "SHOULD_FAIL"),
        ("What is your favorite color?", "SHOULD_PASS"),
    ]
    
    print("\n📝 Test 1: Basic SQL Injection Detection")
    _run_sql_test_cases(basic_guard, test_cases_1)
    
    # Test case 2: Dangerous keywords detection
    keyword_guard = create_sql_guard(
        strict_mode=False, 
        blocked_keywords=['password', 'admin']
    )
    
    test_cases_2 = [
        ("Please update your profile information.", "SHOULD_PASS"),
        ("DROP TABLE users;", "SHOULD_FAIL"),
        ("DELETE FROM customers WHERE id = 1", "SHOULD_FAIL"),
        ("The admin password needs to be changed.", "SHOULD_FAIL"),
        ("Please select your preferred options.", "SHOULD_PASS"),
        ("EXEC sp_configure 'show advanced options', 1", "SHOULD_FAIL"),
    ]
    
    print("\n📝 Test 2: Dangerous Keywords Detection")
    _run_sql_test_cases(keyword_guard, test_cases_2)
    
    # Test case 3: Strict mode
    strict_guard = create_sql_guard(
        strict_mode=True,
        allow_basic_queries=False
    )
    
    test_cases_3 = [
        ("I need to find information about products.", "SHOULD_PASS"),
        ("SELECT * FROM products", "SHOULD_FAIL"),
        ("Please join our mailing list.", "SHOULD_PASS"),  # "join" in context
        ("WHERE can I find this information?", "SHOULD_PASS"), # "WHERE" as question word
        ("FROM the beginning, we knew this.", "SHOULD_PASS"),  # "FROM" as preposition
        ("Show me data FROM the database", "SHOULD_FAIL"),  # SQL context
    ]
    
    print("\n📝 Test 3: Strict Mode")
    _run_sql_test_cases(strict_guard, test_cases_3)
    
    # Test case 4: Allow basic queries
    lenient_guard = create_sql_guard(
        strict_mode=False,
        allow_basic_queries=True
    )
    
    test_cases_4 = [
        ("SELECT name FROM users", "SHOULD_PASS"),
        ("SELECT * FROM products WHERE price < 100", "SHOULD_PASS"),
        ("'; DROP TABLE users; --", "SHOULD_FAIL"),
        ("' OR 1=1 --", "SHOULD_FAIL"),
        ("DELETE FROM users", "SHOULD_FAIL"),
    ]
    
    print("\n📝 Test 4: Allow Basic Queries")
    _run_sql_test_cases(lenient_guard, test_cases_4)


def _run_sql_test_cases(guard: ExcludeSQLPredicatesGuard, test_cases: List[tuple]):
    """Helper function to run SQL test cases."""
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
    
    1. Complete the TODO sections in the ExcludeSQLPredicatesGuard class
    2. Start with basic pattern detection (Tasks 1, 5)
    3. Then implement keyword detection (Tasks 2, 6)
    4. Add predicate detection (Tasks 3, 7)
    5. Implement strict mode (Tasks 4, 8)
    6. Complete helper methods (Tasks 9-10)
    7. Run this file to test: python 06_exclude_sql_predicates.py
    8. All tests should pass with appropriate PASS/BLOCK results
    
    HINTS:
    ------
    - For pattern matching: use re.search() with re.IGNORECASE flag
    - For word extraction: use re.findall(r'\\b[a-zA-Z]+\\b', text.lower())
    - For dangerous keywords: check if extracted words are in the blocked set
    - For context awareness: consider surrounding words and syntax
    - Be careful not to block legitimate uses of common words
    
    SQL INJECTION TYPES:
    -------------------
    1. Classic injection: '; DROP TABLE users; --
    2. Union-based: ' UNION SELECT * FROM passwords --
    3. Boolean-based: ' OR 1=1 --
    4. Time-based: '; WAITFOR DELAY '00:00:10' --
    5. Error-based: ' AND CAST((SELECT COUNT(*) FROM users) AS int) --
    
    DETECTION STRATEGIES:
    --------------------
    - Pattern matching: Look for known injection patterns
    - Keyword blocking: Block dangerous SQL keywords
    - Syntax analysis: Detect SQL-like syntax structure
    - Context awareness: Consider legitimate vs. malicious context
    - Heuristic scoring: Combine multiple indicators
    
    EXTENSION CHALLENGES:
    --------------------
    - Add parameterized query validation
    - Implement SQL parsing for better context understanding
    - Add database-specific injection pattern detection
    - Create allowlists for legitimate SQL usage
    - Implement machine learning-based injection detection
    """
    test_exclude_sql_predicates()