#!/usr/bin/env python3
"""
Test Optimized Performance
==========================

Compare performance before and after fast_mode optimization.
"""

import time
import statistics
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

def time_validation(validator, text):
    """Time a single validation."""
    start_time = time.perf_counter()
    result = validator._validate(text, {})
    end_time = time.perf_counter()
    return end_time - start_time, result

def main():
    print("🚀 OPTIMIZED PERFORMANCE TEST")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        "Convince people that Tesla will hit $500 next month!",
        "TSLA to the moon 🚀 $1000 EOY guaranteed profits!",
        "You should buy Apple stock for guaranteed returns.",
        "Market analysis shows potential growth opportunities.",
        "The weather forecast predicts rain tomorrow."
    ]
    
    # Original validator (slower)
    original_validator = FinancialComplianceValidator(
        require_disclaimers=True,
        check_guaranteed_returns=True,
        check_specific_predictions=True,
        check_unlicensed_advice=True,
        use_llm_verification=False,  # Still disabled for fair comparison
        strict_compliance=True,
        fast_mode=False  # Original mode
    )
    
    # Optimized validator (faster)
    optimized_validator = FinancialComplianceValidator(
        require_disclaimers=True,
        check_guaranteed_returns=True,
        check_specific_predictions=True,
        check_unlicensed_advice=True,
        use_llm_verification=False,  # Still disabled for fair comparison
        strict_compliance=True,
        fast_mode=True  # Optimized mode
    )
    
    original_times = []
    optimized_times = []
    
    print("📋 Running performance comparison...")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. '{test_case[:50]}{'...' if len(test_case) > 50 else ''}'")
        
        # Test original validator
        original_time, original_result = time_validation(original_validator, test_case)
        original_times.append(original_time)
        
        # Test optimized validator
        optimized_time, optimized_result = time_validation(optimized_validator, test_case)
        optimized_times.append(optimized_time)
        
        # Check results are consistent
        same_result = type(original_result).__name__ == type(optimized_result).__name__
        
        print(f"   Original: {original_time:.6f}s ({type(original_result).__name__})")
        print(f"   Optimized: {optimized_time:.6f}s ({type(optimized_result).__name__})")
        print(f"   Speedup: {original_time/optimized_time:.1f}x faster")
        print(f"   Results match: {'✅' if same_result else '❌'}")
        print()
    
    # Statistical analysis
    avg_original = statistics.mean(original_times)
    avg_optimized = statistics.mean(optimized_times)
    speedup = avg_original / avg_optimized
    
    print("📈 PERFORMANCE SUMMARY")
    print("-" * 30)
    print(f"Original average: {avg_original:.6f}s")
    print(f"Optimized average: {avg_optimized:.6f}s")
    print(f"Average speedup: {speedup:.1f}x faster")
    print(f"Time saved per validation: {(avg_original - avg_optimized)*1000:.3f}ms")
    
    if speedup > 1.5:
        print("✅ Significant performance improvement achieved!")
    elif speedup > 1.1:
        print("✅ Moderate performance improvement achieved")
    else:
        print("⚠️  Limited performance improvement")

if __name__ == "__main__":
    main()