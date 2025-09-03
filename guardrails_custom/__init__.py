"""
Custom Guardrails Package
========================

Production-ready custom validators demonstrating advanced Guardrails AI patterns.

Available Validators:
- FinancialComplianceValidator: Comprehensive regulatory compliance for financial content

Usage:
    from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator
    
    # Create validator
    validator = FinancialComplianceValidator(
        require_disclaimers=True,
        check_guaranteed_returns=True
    )
    
    # Use with Guard
    from guardrails import Guard
    guard = Guard()
    guard.use(validator)
"""

__version__ = "1.0.0"