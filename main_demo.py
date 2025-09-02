#!/usr/bin/env python3
"""
Guardrails AI Showcase Demo

This script demonstrates various guardrails implementations including:
- Basic: Competitor mention blocking, Format validation
- Advanced: Psychological manipulation detection, Infrastructure validation, Logical fallacy detection

Usage:
    python main_demo.py [--interactive] [--verbose]
"""

import sys
import json
import argparse
from typing import Dict, Any, List
from guardrails_showcase.basic.competitor_blocking import demo_competitor_blocking
from guardrails_showcase.basic.format_validator import demo_format_validation
from guardrails_showcase.advanced.psychological_manipulation import demo_manipulation_detection
from guardrails_showcase.advanced.infrastructure_validation import demo_infrastructure_validation
from guardrails_showcase.advanced.logical_fallacy_detection import demo_fallacy_detection


def print_separator(title: str, width: int = 80):
    """Print a formatted separator with title"""
    print("\n" + "=" * width)
    print(f" {title} ".center(width))
    print("=" * width)


def print_results(results: List[Dict[str, Any]], verbose: bool = False):
    """Print test results in a formatted way"""
    for i, result in enumerate(results, 1):
        status_color = "\033[92m" if result["status"] in ["PASSED", "PASS"] else "\033[91m"
        reset_color = "\033[0m"
        
        print(f"\n{i}. Input: {result['input'][:60]}{'...' if len(result['input']) > 60 else ''}")
        print(f"   Status: {status_color}{result['status']}{reset_color}")
        
        if result["status"] in ["BLOCKED", "FAILED"] and "reason" in result:
            if verbose:
                print(f"   Reason: {result['reason']}")
            else:
                reason = result['reason'][:80] + "..." if len(result['reason']) > 80 else result['reason']
                print(f"   Reason: {reason}")


def run_basic_demos(verbose: bool = False):
    """Run all basic guardrails demos"""
    print_separator("BASIC GUARDRAILS DEMONSTRATION")
    
    # Competitor Blocking Demo
    print("\n📛 Competitor Mention Blocking")
    print("-" * 40)
    try:
        results = demo_competitor_blocking()
        print_results(results, verbose)
        
        passed = sum(1 for r in results if r["status"] == "PASSED")
        total = len(results)
        print(f"\nResults: {passed}/{total} passed")
        
    except Exception as e:
        print(f"❌ Error running competitor blocking demo: {e}")
    
    # Format Validation Demo
    print("\n📝 Format Validation")
    print("-" * 40)
    try:
        results_dict = demo_format_validation()
        
        for validator_type, results in results_dict.items():
            print(f"\n{validator_type.replace('_', ' ').title()}:")
            print_results(results, verbose)
            
            passed = sum(1 for r in results if r["status"] == "PASSED")
            total = len(results)
            print(f"Results: {passed}/{total} passed")
            
    except Exception as e:
        print(f"❌ Error running format validation demo: {e}")


def run_advanced_demos(verbose: bool = False):
    """Run all advanced guardrails demos"""
    print_separator("ADVANCED GUARDRAILS DEMONSTRATION")
    
    # Psychological Manipulation Detection
    print("\n🧠 Psychological Manipulation Detection")
    print("-" * 50)
    try:
        results = demo_manipulation_detection()
        print_results(results, verbose)
        
        passed = sum(1 for r in results if r["status"] == "PASSED")
        total = len(results)
        print(f"\nResults: {passed}/{total} passed")
        
    except Exception as e:
        print(f"❌ Error running manipulation detection demo: {e}")
    
    # Infrastructure Validation
    print("\n🌐 Infrastructure Validation")
    print("-" * 40)
    try:
        results_dict = demo_infrastructure_validation()
        
        for validator_type, results in results_dict.items():
            print(f"\n{validator_type.upper()}:")
            print_results(results, verbose)
            
            passed = sum(1 for r in results if r["status"] == "PASSED")
            total = len(results)
            print(f"Results: {passed}/{total} passed")
            
    except Exception as e:
        print(f"❌ Error running infrastructure validation demo: {e}")
    
    # Logical Fallacy Detection
    print("\n🤔 Logical Fallacy Detection")
    print("-" * 40)
    try:
        results_dict = demo_fallacy_detection()
        
        for detector_type, results in results_dict.items():
            print(f"\n{detector_type.replace('_', ' ').title()}:")
            print_results(results, verbose)
            
            passed = sum(1 for r in results if r["status"] == "PASSED")
            total = len(results)
            print(f"Results: {passed}/{total} passed")
            
    except Exception as e:
        print(f"❌ Error running fallacy detection demo: {e}")


def interactive_mode():
    """Run interactive demo where user can test their own inputs"""
    print_separator("INTERACTIVE MODE")
    
    from guardrails_showcase.basic.competitor_blocking import create_competitor_guard, TECH_COMPETITORS
    from guardrails_showcase.basic.format_validator import create_format_guard
    from guardrails_showcase.advanced.psychological_manipulation import create_manipulation_guard
    from guardrails_showcase.advanced.infrastructure_validation import create_infrastructure_guard
    from guardrails_showcase.advanced.logical_fallacy_detection import create_fallacy_guard
    
    # Initialize guards (basic and advanced)
    guards = {
        "1": ("Competitor Blocking", create_competitor_guard(TECH_COMPETITORS)),
        "2": ("Two Words All Caps", create_format_guard('two_words_caps')),
        "3": ("Email Format", create_format_guard('email')),
        "4": ("Phone Format", create_format_guard('phone')),
        "5": ("URL Validation", create_infrastructure_guard('url', blocked_domains=['spam.com'])),
        "6": ("Manipulation Detection", create_manipulation_guard(use_llm=True)),
        "7": ("Logical Fallacy Detection", create_fallacy_guard("fallacy", use_llm=True)),
        "8": ("IP Address Validation", create_infrastructure_guard('ip', allow_private=False))
    }
    
    print("\nAvailable Guardrails:")
    for key, (name, _) in guards.items():
        print(f"{key}. {name}")
    
    while True:
        print("\n" + "-" * 50)
        choice = input("\nSelect a guardrail (1-8) or 'quit' to exit: ").strip()
        
        if choice.lower() in ['quit', 'q', 'exit']:
            break
        
        if choice not in guards:
            print("Invalid choice. Please select 1-8.")
            continue
        
        guard_name, guard = guards[choice]
        print(f"\nTesting {guard_name}")
        
        text = input("Enter text to validate: ").strip()
        if not text:
            print("Empty input, skipping...")
            continue
        
        try:
            result = guard.validate(text)
            print("✅ PASSED: Text is valid")
            if result != text:
                print(f"Processed output: {result}")
        except Exception as e:
            print(f"❌ BLOCKED: {e}")


def main():
    """Main demo function"""
    parser = argparse.ArgumentParser(description="Guardrails AI Showcase Demo")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed output")
    parser.add_argument("--basic-only", action="store_true",
                       help="Run only basic guardrails demos")
    parser.add_argument("--advanced-only", action="store_true",
                       help="Run only advanced guardrails demos")
    
    args = parser.parse_args()
    
    print_separator("GUARDRAILS AI SHOWCASE", 80)
    print("🛡️  Demonstrating various AI content validation guardrails")
    print("🎯 From basic pattern matching to advanced LLM-based detection")
    
    if args.interactive:
        interactive_mode()
        return
    
    try:
        if not args.advanced_only:
            run_basic_demos(args.verbose)
        
        if not args.basic_only:
            run_advanced_demos(args.verbose)
        
        print_separator("DEMO COMPLETE", 80)
        print("✅ All guardrails demonstrations completed!")
        print("\n💡 Tips:")
        print("   • Use --interactive to test your own inputs")
        print("   • Use --verbose for detailed error messages")
        print("   • Configure API keys in .env file for LLM-based guardrails")
        print("\n📚 Check individual modules for more configuration options")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()