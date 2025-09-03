"""
Financial Advice Compliance Validator
====================================

A comprehensive custom validator that ensures financial content complies with 
regulatory requirements and best practices.

This validator demonstrates:
- Multi-stage validation workflows
- Topic detection combined with compliance checking
- LLM integration for advanced analysis
- Regulatory pattern matching
- Disclaimer requirement enforcement

Usage:
    from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator
    
    # Create guard with financial compliance
    guard = Guard()
    guard.use(FinancialComplianceValidator(
        require_disclaimers=True,
        check_guaranteed_returns=True,
        strict_mode=False
    ))
    
    # Validate financial content
    result = guard.validate("You should buy Apple stock for guaranteed profits!")
"""

import os
import re
from typing import List, Dict, Set, Optional, Tuple, Any
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)
import requests
from dotenv import load_dotenv

load_dotenv()


@register_validator(name="financial-compliance", data_type="string")
class FinancialComplianceValidator(Validator):
    """
    A comprehensive validator for financial advice compliance.
    
    This validator combines topic detection with regulatory compliance checking
    to ensure financial content meets legal and ethical standards.
    """
    
    def __init__(
        self,
        require_disclaimers: bool = True,
        check_guaranteed_returns: bool = True,
        check_specific_predictions: bool = True,
        check_unlicensed_advice: bool = True,
        use_llm_verification: bool = True,
        strict_compliance: bool = False,
        **kwargs
    ):
        """
        Initialize the financial compliance validator.
        
        Args:
            require_disclaimers: Require appropriate disclaimers for financial advice
            check_guaranteed_returns: Block guaranteed return language
            check_specific_predictions: Flag overly specific predictions
            check_unlicensed_advice: Check for unlicensed advice indicators
            use_llm_verification: Use LLM for advanced compliance checking
            strict_compliance: Apply strictest regulatory standards
        """
        super().__init__(**kwargs)
        self.require_disclaimers = require_disclaimers
        self.check_guaranteed_returns = check_guaranteed_returns
        self.check_specific_predictions = check_specific_predictions
        self.check_unlicensed_advice = check_unlicensed_advice
        self.use_llm_verification = use_llm_verification
        self.strict_compliance = strict_compliance
        
        # Financial topic keywords for detection
        self.financial_keywords = {
            "invest", "investment", "portfolio", "stock", "stocks", "bond", "bonds",
            "etf", "mutual fund", "401k", "ira", "retirement", "dividend", "yield",
            "trade", "trading", "buy", "sell", "broker", "market", "exchange",
            "bull market", "bear market", "volatility", "risk", "return", "roi",
            "financial advice", "investment advice", "recommend", "suggestion",
            "strategy", "allocation", "diversification", "asset", "wealth",
            "crypto", "cryptocurrency", "bitcoin", "real estate", "commodities",
            "securities", "equity", "debt", "capital", "finance", "financial"
        }
        
        # Prohibited guarantee language patterns
        self.guaranteed_return_patterns = [
            r"\b(guarantee[sd]?|assured|certain|definite|promised)\b.*\b(returns?|profits?|gains?|income)\b",
            r"\b(guarantee[sd]?)\b.*\bmake.*\b(money|returns?|profits?)\b",
            r"\b(risk[- ]free|no[- ]risk|zero[- ]risk)\b",
            r"\bwill\s+(definitely|certainly|surely)\s+.*\b(increase|rise|grow|profit)\b",
            r"\b100%\s+(safe|secure|guaranteed)\b",
            r"\bcannot\s+(lose|fail)\b.*\b(money|investment)\b",
            r"\bsure\s+(thing|bet|profit)\b",
            r"\bno\s+(chance|risk)\s+of\s+loss\b"
        ]
        
        # Overly specific prediction patterns
        self.specific_prediction_patterns = [
            r"\b(will|going to)\s+.*\b(hit|reach|be worth)\s+\$[\d,]+\b",
            r"\b[A-Z]{2,5}\s+will\s+(hit|reach)\s+\$[\d,]+\b",  # Stock will hit price
            r"\bby\s+(next\s+week|next\s+month|\d{1,2}/\d{1,2}/\d{4})\b.*\b(price|value)\b",
            r"\bexactly\s+\d+%\s+(gain|return|profit)\b",
            r"\bwill\s+be\s+worth\s+exactly\s+\$[\d,]+\b",
            r"\b(tomorrow|next\s+week|this\s+month)\s+.*\b(will\s+be|expect)\b",
            r"\bpredicting?\s+.*\$[\d,]+\s+by\b"
        ]
        
        # Required disclaimer keywords/phrases
        self.disclaimer_keywords = {
            "not financial advice", "not investment advice", "consult", "professional",
            "do your own research", "past performance", "risk", "disclaimer",
            "opinion only", "educational purposes", "seek advice", "qualified advisor",
            "investment professional", "financial planner", "due diligence"
        }
        
        # Financial advice indicators
        self.advice_indicators = [
            r"\b(should|must|recommend|suggest)\s+(buy|sell|invest|trade)\b",
            r"\b(best|top|perfect)\s+(stock|investment|strategy)\b",
            r"\b(my\s+advice|i\s+recommend|you\s+should)\b",
            r"\b(time\s+to\s+buy|now\s+is\s+the\s+time)\b",
            r"\b(buy\s+now|sell\s+now|act\s+fast)\b",
            r"\b(strong\s+buy|strong\s+sell)\b"
        ]
        
        # Licensing claim patterns
        self.licensing_patterns = [
            r"\bas\s+a\s+financial\s+advisor\b",
            r"\bi\s+am\s+a\s+licensed\b",
            r"\bmy\s+professional\s+opinion\b",
            r"\bfiduciary\s+(advice|duty)\b",
            r"\bcertified\s+financial\s+planner\b",
            r"\bregistered\s+investment\s+advisor\b"
        ]
    
    def _validate(self, value: str, metadata: Dict[str, Any]) -> ValidationResult:
        """
        Validate financial content for regulatory compliance.
        
        Returns:
            ValidationResult: PassResult if compliant, FailResult with details if not
        """
        if not value or not isinstance(value, str):
            return PassResult()
        
        # Stage 1: Check if this content contains financial advice
        if not self._contains_financial_content(value):
            return PassResult()  # Not financial content, no compliance needed
        
        compliance_issues = []
        
        # Stage 2: Run compliance checks
        if self.check_guaranteed_returns:
            guaranteed_issues = self._check_guaranteed_returns(value)
            compliance_issues.extend(guaranteed_issues)
        
        if self.check_specific_predictions:
            prediction_issues = self._check_specific_predictions(value)
            compliance_issues.extend(prediction_issues)
        
        if self.require_disclaimers:
            disclaimer_issues = self._check_disclaimers(value)
            compliance_issues.extend(disclaimer_issues)
        
        if self.check_unlicensed_advice:
            licensing_issues = self._check_unlicensed_advice(value)
            compliance_issues.extend(licensing_issues)
        
        if self.use_llm_verification:
            llm_issues = self._llm_compliance_check(value)
            compliance_issues.extend(llm_issues)
        
        # Stage 3: Determine result
        if compliance_issues:
            issues_summary = "; ".join(compliance_issues)
            return FailResult(
                error_message=f"Financial compliance violations: {issues_summary}",
                fix_value=self._suggest_compliant_version(value, compliance_issues)
            )
        
        return PassResult()
    
    def _contains_financial_content(self, text: str) -> bool:
        """Check if text contains financial advice or investment content."""
        text_lower = text.lower()
        
        # Count financial keywords
        financial_keyword_count = sum(1 for keyword in self.financial_keywords if keyword in text_lower)
        
        # Check for advice indicators
        advice_pattern_count = sum(1 for pattern in self.advice_indicators if re.search(pattern, text_lower))
        
        # Financial content if 2+ keywords OR 1+ advice patterns
        return financial_keyword_count >= 2 or advice_pattern_count >= 1
    
    def _check_guaranteed_returns(self, text: str) -> List[str]:
        """Check for prohibited guaranteed return language."""
        issues = []
        text_lower = text.lower()
        
        for pattern in self.guaranteed_return_patterns:
            if re.search(pattern, text_lower):
                issues.append("Contains prohibited guaranteed return language")
                break
        
        return issues
    
    def _check_specific_predictions(self, text: str) -> List[str]:
        """Check for overly specific price predictions or timing."""
        issues = []
        text_lower = text.lower()
        
        for pattern in self.specific_prediction_patterns:
            if re.search(pattern, text_lower):
                # Check if prediction has uncertainty language
                uncertainty_words = {"might", "could", "may", "possibly", "perhaps", "likely", "potentially"}
                has_uncertainty = any(word in text_lower for word in uncertainty_words)
                
                if not has_uncertainty:
                    issues.append("Contains overly specific predictions without uncertainty language")
                    break
        
        return issues
    
    def _check_disclaimers(self, text: str) -> List[str]:
        """Check if appropriate disclaimers are present."""
        issues = []
        text_lower = text.lower()
        
        # Check if text contains advice indicators
        has_advice = any(re.search(pattern, text_lower) for pattern in self.advice_indicators)
        
        if has_advice:
            # Check if disclaimers are present
            has_disclaimer = any(disclaimer in text_lower for disclaimer in self.disclaimer_keywords)
            
            if not has_disclaimer:
                issues.append("Financial advice provided without required disclaimers")
        
        return issues
    
    def _check_unlicensed_advice(self, text: str) -> List[str]:
        """Check for indicators of potentially unlicensed financial advice."""
        issues = []
        text_lower = text.lower()
        
        # Check for licensing claims
        has_licensing_claim = any(re.search(pattern, text_lower) for pattern in self.licensing_patterns)
        has_advice = any(re.search(pattern, text_lower) for pattern in self.advice_indicators)
        
        if has_licensing_claim and has_advice:
            # Look for licensing disclaimers
            licensing_disclaimers = {"not a licensed", "not a financial advisor", "not professional advice"}
            has_licensing_disclaimer = any(disclaimer in text_lower for disclaimer in licensing_disclaimers)
            
            if not has_licensing_disclaimer:
                issues.append("Potential unlicensed financial advice - verify credentials")
        
        return issues
    
    def _llm_compliance_check(self, text: str) -> List[str]:
        """Use LLM for advanced financial compliance checking."""
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return []
        
        prompt = f"""
        Analyze this text for financial advice compliance issues:

        Text: "{text}"

        Check for:
        1. Investment advice without disclaimers
        2. Guaranteed return promises
        3. Overly specific predictions without caveats
        4. Unlicensed advisor claims
        5. SEC/FINRA regulatory red flags

        Respond with:
        - "COMPLIANT" if no major issues
        - "VIOLATIONS: [specific issues]" if problems exist
        """
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 300
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                llm_response = result["choices"][0]["message"]["content"].strip()
                
                if llm_response.startswith("VIOLATIONS"):
                    issues_text = llm_response.replace("VIOLATIONS:", "").strip()
                    return [f"LLM detected: {issues_text}"]
            
            return []
            
        except Exception:
            return []  # Fail-safe: don't block on API errors
    
    def _suggest_compliant_version(self, original_text: str, issues: List[str]) -> str:
        """Suggest a compliant version of the text."""
        fixed_text = original_text
        
        # Add disclaimer if missing
        if any("disclaimer" in issue for issue in issues):
            fixed_text += "\n\nDisclaimer: This is not financial advice. Please consult with a qualified financial professional before making investment decisions."
        
        # Soften guaranteed language
        if any("guaranteed" in issue for issue in issues):
            fixed_text = re.sub(r"\bguarantee[sd]?\b", "potentially", fixed_text, flags=re.IGNORECASE)
            fixed_text = re.sub(r"\bcannot lose\b", "may have lower risk", fixed_text, flags=re.IGNORECASE)
        
        # Add uncertainty to predictions
        if any("specific prediction" in issue for issue in issues):
            fixed_text = re.sub(r"\bwill hit\b", "might reach", fixed_text, flags=re.IGNORECASE)
            fixed_text = re.sub(r"\bwill be\b", "could be", fixed_text, flags=re.IGNORECASE)
        
        return fixed_text


def create_financial_guard(**kwargs):
    """
    Factory function to create a Guard with financial compliance validation.
    
    Usage:
        guard = create_financial_guard(
            require_disclaimers=True,
            check_guaranteed_returns=True,
            strict_compliance=False
        )
        
        result = guard.validate("Buy AAPL stock now for guaranteed profits!")
    """
    try:
        from guardrails import Guard
        
        guard = Guard()
        guard.use(FinancialComplianceValidator(**kwargs))
        return guard
        
    except ImportError:
        # Fallback for environments without full Guardrails
        print("Warning: Full Guardrails library not available. Using standalone validator.")
        return FinancialComplianceValidator(**kwargs)


# Demo and testing functions
def demo_financial_compliance():
    """Demonstrate the financial compliance validator with various test cases."""
    
    print("🛡️  FINANCIAL COMPLIANCE VALIDATOR DEMO")
    print("=" * 70)
    print("This demonstrates a complete custom validator for financial content compliance.")
    print()
    
    # Create validator instance
    validator = FinancialComplianceValidator(
        require_disclaimers=True,
        check_guaranteed_returns=True,
        check_specific_predictions=True,
        use_llm_verification=False  # Disable for demo speed
    )
    
    # Test cases with expected outcomes
    test_cases = [
        # Should pass
        ("Consider diversified investing for long-term wealth building. This is not financial advice - consult a professional.", 
         "✅ SHOULD PASS", "Good advice with proper disclaimer"),
        
        ("Market analysis suggests tech stocks may see growth opportunities in the coming quarters.", 
         "✅ SHOULD PASS", "General market commentary without specific advice"),
        
        # Should fail - guaranteed returns
        ("I guarantee you'll make 20% returns with this investment strategy!", 
         "❌ SHOULD FAIL", "Contains guaranteed return language"),
        
        ("This is a risk-free investment that cannot lose money!", 
         "❌ SHOULD FAIL", "Risk-free claims are prohibited"),
        
        # Should fail - specific predictions
        ("AAPL stock will hit $200 by next month based on my analysis.", 
         "❌ SHOULD FAIL", "Overly specific price prediction"),
        
        ("Bitcoin will be worth exactly $100,000 by December 31st.", 
         "❌ SHOULD FAIL", "Specific prediction without uncertainty"),
        
        # Should fail - missing disclaimers
        ("You should buy Tesla stock immediately - it's the perfect investment!", 
         "❌ SHOULD FAIL", "Investment advice without disclaimers"),
        
        ("My recommendation is to sell all your tech stocks and buy gold.", 
         "❌ SHOULD FAIL", "Direct advice without proper warnings"),
        
        # Edge cases
        ("The weather forecast shows rain tomorrow.", 
         "✅ SHOULD PASS", "Non-financial content should pass"),
        
        ("I love investing in index funds for retirement planning. Not financial advice.", 
         "✅ SHOULD PASS", "Personal opinion with disclaimer"),
    ]
    
    print("🧪 RUNNING COMPLIANCE TESTS")
    print("-" * 70)
    
    for i, (text, expected, description) in enumerate(test_cases, 1):
        print(f"\\n{i}. {description}")
        print(f"   Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"   Expected: {expected}")
        
        # Run validation
        try:
            # Use the _validate method directly for demo
            result = validator._validate(text, {})
            
            if hasattr(result, 'error_message'):
                # FailResult
                actual = "❌ BLOCKED"
                print(f"   Actual: {actual}")
                print(f"   Reason: {result.error_message}")
                if hasattr(result, 'fix_value') and result.fix_value:
                    print(f"   Suggested fix: '{result.fix_value[:60]}...'")
            else:
                # PassResult
                actual = "✅ PASSED"
                print(f"   Actual: {actual}")
            
            # Check if result matches expectation
            expected_pass = "SHOULD PASS" in expected
            actual_pass = actual == "✅ PASSED"
            
            if expected_pass == actual_pass:
                print("   Status: ✅ Test passed")
            else:
                print("   Status: ⚠️  Unexpected result")
                
        except Exception as e:
            print(f"   Actual: ❌ ERROR - {e}")
            print("   Status: ❌ Test failed with exception")
    
    print("\\n" + "=" * 70)
    print("🎯 DEMO COMPLETE")
    print("\\nThis validator demonstrates:")
    print("• Multi-stage validation (topic detection → compliance checking)")
    print("• Pattern-based compliance rules (regex + keyword matching)")
    print("• LLM integration for advanced analysis")
    print("• Automatic fix suggestions for common violations")
    print("• Regulatory compliance for financial content (SEC/FINRA guidelines)")
    print("\\nUse this as a foundation for building domain-specific validators!")


if __name__ == "__main__":
    demo_financial_compliance()