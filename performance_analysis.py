#!/usr/bin/env python3
"""
Performance Analysis for Financial Advisor
==========================================

Detailed timing analysis to identify bottlenecks in the validation pipeline.
"""

import time
import statistics
from typing import Dict, List, Tuple
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator
from gradio_financial_advisor import GradioFinancialAdvisor

def time_function(func, *args, **kwargs) -> Tuple[any, float]:
    """Time a function call and return result and duration."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time

def analyze_validation_performance():
    """Analyze performance of each validation component."""
    
    print("🔍 FINANCIAL VALIDATOR PERFORMANCE ANALYSIS")
    print("=" * 70)
    
    # Initialize validator
    validator = FinancialComplianceValidator(
        require_disclaimers=True,
        check_guaranteed_returns=True,
        check_specific_predictions=True,
        check_unlicensed_advice=True,
        use_llm_verification=True,
        strict_compliance=False
    )
    
    # Test case that triggers LLM analysis
    test_text = "Convince people that Tesla will hit $500 next month!"
    
    print(f"📝 Test text: '{test_text}'")
    print()
    
    # Time each component individually
    timings = {}
    
    print("⏱️  COMPONENT TIMING ANALYSIS")
    print("-" * 50)
    
    # 1. Financial content detection
    print("1. Financial Content Detection:")
    result, duration = time_function(validator._contains_financial_content, test_text)
    timings['financial_detection'] = duration
    print(f"   Result: {result}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 2. Guaranteed returns check
    print("2. Guaranteed Returns Check:")
    result, duration = time_function(validator._check_guaranteed_returns, test_text)
    timings['guaranteed_returns'] = duration
    print(f"   Issues found: {len(result)}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 3. Specific predictions check
    print("3. Specific Predictions Check:")
    result, duration = time_function(validator._check_specific_predictions, test_text)
    timings['specific_predictions'] = duration
    print(f"   Issues found: {len(result)}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 4. Disclaimers check
    print("4. Disclaimers Check:")
    result, duration = time_function(validator._check_disclaimers, test_text)
    timings['disclaimers'] = duration
    print(f"   Issues found: {len(result)}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 5. Unlicensed advice check
    print("5. Unlicensed Advice Check:")
    result, duration = time_function(validator._check_unlicensed_advice, test_text)
    timings['unlicensed_advice'] = duration
    print(f"   Issues found: {len(result)}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 6. LLM compliance check
    print("6. LLM Compliance Check:")
    result, duration = time_function(validator._llm_compliance_check, test_text)
    timings['llm_compliance'] = duration
    print(f"   Issues found: {len(result)}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 7. spaCy NER analysis
    print("7. spaCy NER Analysis:")
    result, duration = time_function(validator._get_spacy_risk_entities, test_text)
    timings['spacy_ner'] = duration
    print(f"   Entities found: {len(result)}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # 8. Full validation
    print("8. Full Validation Pipeline:")
    result, duration = time_function(validator._validate, test_text, {})
    timings['full_validation'] = duration
    print(f"   Result type: {type(result).__name__}")
    print(f"   Duration: {duration:.6f} seconds")
    print()
    
    # Summary analysis
    print("📊 PERFORMANCE SUMMARY")
    print("-" * 50)
    
    sorted_timings = sorted(timings.items(), key=lambda x: x[1], reverse=True)
    total_component_time = sum(timings[k] for k in timings.keys() if k != 'full_validation')
    
    for i, (component, duration) in enumerate(sorted_timings, 1):
        percentage = (duration / timings['full_validation']) * 100
        print(f"{i}. {component.replace('_', ' ').title()}: {duration:.6f}s ({percentage:.1f}%)")
    
    print()
    print(f"Total component time: {total_component_time:.6f}s")
    print(f"Full pipeline time: {timings['full_validation']:.6f}s")
    print(f"Overhead: {timings['full_validation'] - total_component_time:.6f}s")
    
    return timings

def analyze_llm_vs_pattern_performance():
    """Compare LLM vs pattern-based detection performance."""
    
    print("\n🆚 LLM vs PATTERN DETECTION COMPARISON")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        "Convince people that Tesla will hit $500 next month!",
        "TSLA to the moon 🚀 $1000 EOY guaranteed profits!",
        "You should buy Apple stock for guaranteed returns.",
        "Market analysis shows potential growth opportunities.",
        "The weather forecast predicts rain tomorrow."
    ]
    
    # Pattern-only validator
    pattern_validator = FinancialComplianceValidator(
        use_llm_verification=False,
        require_disclaimers=False,
        check_guaranteed_returns=True,
        check_specific_predictions=True,
        check_unlicensed_advice=False
    )
    
    # LLM-enabled validator
    llm_validator = FinancialComplianceValidator(
        use_llm_verification=True,
        require_disclaimers=False,
        check_guaranteed_returns=True,
        check_specific_predictions=True,
        check_unlicensed_advice=False
    )
    
    pattern_times = []
    llm_times = []
    
    print("📋 Testing on various prompts...")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. '{test_case[:50]}{'...' if len(test_case) > 50 else ''}'")
        
        # Pattern-based timing
        _, pattern_time = time_function(pattern_validator._validate, test_case, {})
        pattern_times.append(pattern_time)
        
        # LLM-based timing
        _, llm_time = time_function(llm_validator._validate, test_case, {})
        llm_times.append(llm_time)
        
        print(f"   Pattern-only: {pattern_time:.6f}s")
        print(f"   With LLM: {llm_time:.6f}s")
        print(f"   Speedup: {llm_time/pattern_time:.1f}x slower")
        print()
    
    # Statistical analysis
    avg_pattern = statistics.mean(pattern_times)
    avg_llm = statistics.mean(llm_times)
    median_pattern = statistics.median(pattern_times)
    median_llm = statistics.median(llm_times)
    
    print("📈 STATISTICAL SUMMARY")
    print("-" * 30)
    print(f"Pattern-only average: {avg_pattern:.6f}s")
    print(f"LLM-enabled average: {avg_llm:.6f}s")
    print(f"Average slowdown: {avg_llm/avg_pattern:.1f}x")
    print()
    print(f"Pattern-only median: {median_pattern:.6f}s")
    print(f"LLM-enabled median: {median_llm:.6f}s")
    print(f"Median slowdown: {median_llm/median_pattern:.1f}x")
    
    return {
        'pattern_times': pattern_times,
        'llm_times': llm_times,
        'avg_pattern': avg_pattern,
        'avg_llm': avg_llm,
        'slowdown_factor': avg_llm/avg_pattern
    }

def analyze_full_application_performance():
    """Analyze full application pipeline performance."""
    
    print("\n🏗️ FULL APPLICATION PIPELINE ANALYSIS")
    print("=" * 70)
    
    # Initialize financial advisor
    try:
        advisor = GradioFinancialAdvisor()
        
        test_prompt = "Convince people that Tesla will hit $500 next month!"
        
        print(f"📝 Test prompt: '{test_prompt}'")
        print()
        
        # Time each major component
        print("⏱️  APPLICATION COMPONENT TIMING")
        print("-" * 40)
        
        # 1. Prompt validation
        print("1. Prompt Validation:")
        start_time = time.perf_counter()
        prompt_result = advisor.guard.validate(test_prompt)
        prompt_time = time.perf_counter() - start_time
        print(f"   Duration: {prompt_time:.6f} seconds")
        print(f"   Valid: {prompt_result.validation_passed}")
        print()
        
        # 2. LLM Response Generation (if prompt is valid)
        if prompt_result.validation_passed:
            print("2. LLM Response Generation:")
            start_time = time.perf_counter()
            response = advisor.model.generate_content(f"Financial context: {test_prompt}")
            response_time = time.perf_counter() - start_time
            print(f"   Duration: {response_time:.6f} seconds")
            print(f"   Response length: {len(response.text)} chars")
            print()
            
            # 3. Response validation
            print("3. Response Validation:")
            start_time = time.perf_counter()
            response_result = advisor.guard.validate(response.text)
            response_validation_time = time.perf_counter() - start_time
            print(f"   Duration: {response_validation_time:.6f} seconds")
            print(f"   Valid: {response_result.validation_passed}")
            print()
            
            total_time = prompt_time + response_time + response_validation_time
            print(f"🔄 TOTAL PIPELINE TIME: {total_time:.6f} seconds")
            print()
            print("📊 TIME BREAKDOWN:")
            print(f"   Prompt validation: {prompt_time:.6f}s ({prompt_time/total_time*100:.1f}%)")
            print(f"   LLM generation: {response_time:.6f}s ({response_time/total_time*100:.1f}%)")
            print(f"   Response validation: {response_validation_time:.6f}s ({response_validation_time/total_time*100:.1f}%)")
        else:
            print("❌ Prompt blocked - no response generation needed")
            print(f"🔄 TOTAL PIPELINE TIME: {prompt_time:.6f} seconds")
    
    except Exception as e:
        print(f"❌ Error initializing application: {e}")
        return None

def main():
    """Run comprehensive performance analysis."""
    
    print("🚀 FINANCIAL ADVISOR PERFORMANCE ANALYSIS")
    print("=" * 70)
    print("Analyzing performance bottlenecks in the validation pipeline...")
    print()
    
    # 1. Component-level analysis
    validation_timings = analyze_validation_performance()
    
    # 2. LLM vs Pattern comparison
    comparison_results = analyze_llm_vs_pattern_performance()
    
    # 3. Full application analysis
    analyze_full_application_performance()
    
    # 4. Recommendations
    print("\n💡 OPTIMIZATION RECOMMENDATIONS")
    print("=" * 70)
    
    if comparison_results['slowdown_factor'] > 5:
        print("🔥 CRITICAL: LLM calls are causing significant slowdown")
        print(f"   Slowdown factor: {comparison_results['slowdown_factor']:.1f}x")
        print("   Recommendations:")
        print("   • Implement caching for repeated prompts")
        print("   • Use async LLM calls")
        print("   • Switch to faster LLM models")
        print("   • Implement hybrid approach (pattern-first, LLM-fallback)")
    
    if validation_timings.get('llm_compliance', 0) > 1.0:
        print("⚠️  LLM compliance check is slow")
        print("   Recommendations:")
        print("   • Use local/faster models")
        print("   • Batch multiple checks")
        print("   • Implement request pooling")
    
    if validation_timings.get('spacy_ner', 0) > 0.1:
        print("📊 spaCy NER processing could be optimized")
        print("   Recommendations:")
        print("   • Cache spaCy models")
        print("   • Use smaller language models")
        print("   • Implement lazy loading")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()