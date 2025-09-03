#!/usr/bin/env python3
"""
Custom Guardrails Demo Runner
============================

Interactive demonstration system for advanced custom guardrails that showcase
the full power and flexibility of the Guardrails AI framework.

These validators demonstrate professional-grade implementations suitable for
production use, complete with proper error handling, LLM integration, and
regulatory compliance features.

Usage:
    python guardrails_custom/demo_runner.py
    python guardrails_custom/demo_runner.py --validator financial
    python guardrails_custom/demo_runner.py --interactive
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple


class CustomGuardrailsDemoRunner:
    """Demo runner for advanced custom guardrails."""
    
    def __init__(self):
        self.validators = {
            "financial": {
                "name": "Financial Advice Compliance Validator",
                "description": "Comprehensive regulatory compliance for financial content",
                "complexity": "Advanced",
                "module": "financial_compliance_validator",
                "features": [
                    "Multi-stage validation workflow",
                    "Topic detection + compliance checking", 
                    "Regulatory pattern matching (SEC/FINRA)",
                    "LLM integration for advanced analysis",
                    "Automatic fix suggestions",
                    "Disclaimer requirement enforcement"
                ],
                "use_cases": [
                    "Investment advice platforms",
                    "Financial content moderation",
                    "Regulatory compliance automation",
                    "Risk management for fintech apps"
                ]
            }
            # Future validators can be added here:
            # "medical": { ... },
            # "legal": { ... },
            # "privacy": { ... }
        }
    
    def show_menu(self):
        """Display the main demo menu."""
        print("=" * 80)
        print("🛡️  CUSTOM GUARDRAILS DEMONSTRATIONS")
        print("=" * 80)
        print("Advanced, production-ready validators showcasing Guardrails AI capabilities")
        print()
        print("Available Custom Validators:")
        print("-" * 80)
        
        for key, validator in self.validators.items():
            print(f"\\n🔧 {validator['name']} ({key})")
            print(f"   {validator['complexity']}")
            print(f"   📝 {validator['description']}")
            print(f"   ✨ Features:")
            for feature in validator['features']:
                print(f"      • {feature}")
            print(f"   🎯 Use Cases:")
            for use_case in validator['use_cases']:
                print(f"      • {use_case}")
        
        print("\\n" + "=" * 80)
        print("💡 About Custom Validators:")
        print("   • These are complete, professional implementations")
        print("   • Suitable for production environments")
        print("   • Demonstrate advanced Guardrails AI patterns")
        print("   • Show integration with external APIs (LLMs)")
        print("   • Include comprehensive error handling and fixes")
        
        print("\\n🚀 Usage:")
        print("   python demo_runner.py --validator financial    # Run financial validator demo")
        print("   python demo_runner.py --interactive            # Interactive mode")
        print("   python demo_runner.py --list                   # Show this menu")
    
    def run_validator_demo(self, validator_key: str):
        """Run a specific validator demonstration."""
        if validator_key not in self.validators:
            print(f"❌ Validator '{validator_key}' not found!")
            print(f"Available validators: {list(self.validators.keys())}")
            return
        
        validator_info = self.validators[validator_key]
        module_name = validator_info['module']
        
        print("=" * 80)
        print(f"🔧 {validator_info['name']} DEMO")
        print("=" * 80)
        print(f"📖 Description: {validator_info['description']}")
        print(f"📊 Complexity: {validator_info['complexity']}")
        print()
        print("🎯 This demonstration will show:")
        for i, feature in enumerate(validator_info['features'], 1):
            print(f"   {i}. {feature}")
        print()
        
        # Import and run the validator demo
        try:
            if validator_key == "financial":
                import sys
                from pathlib import Path
                # Add the current directory to Python path
                current_dir = Path(__file__).parent
                if str(current_dir) not in sys.path:
                    sys.path.insert(0, str(current_dir))
                
                from financial_compliance_validator import demo_financial_compliance
                demo_financial_compliance()
            else:
                print(f"❌ Demo not implemented for {validator_key}")
                
        except ImportError as e:
            print(f"❌ Error importing validator module: {e}")
            print("💡 Make sure all dependencies are installed")
        except Exception as e:
            print(f"❌ Error running demo: {e}")
    
    def run_interactive_mode(self):
        """Run interactive mode for testing validators."""
        print("=" * 80)
        print("🎮 INTERACTIVE CUSTOM VALIDATOR TESTING")
        print("=" * 80)
        print("Test custom validators with your own content!")
        print()
        
        # Select validator
        print("Available validators:")
        for i, (key, validator) in enumerate(self.validators.items(), 1):
            print(f"  {i}. {validator['name']} ({key})")
        
        try:
            validator_choice = input("\\nSelect validator (number or name): ").strip().lower()
            
            # Handle numeric choice
            if validator_choice.isdigit():
                validator_keys = list(self.validators.keys())
                choice_idx = int(validator_choice) - 1
                if 0 <= choice_idx < len(validator_keys):
                    validator_key = validator_keys[choice_idx]
                else:
                    print("❌ Invalid choice")
                    return
            else:
                # Handle name choice
                if validator_choice in self.validators:
                    validator_key = validator_choice
                else:
                    print("❌ Validator not found")
                    return
            
            print(f"\\n🔧 Using {self.validators[validator_key]['name']}")
            print("-" * 50)
            
            # Load validator
            if validator_key == "financial":
                import sys
                from pathlib import Path
                # Add the current directory to Python path
                current_dir = Path(__file__).parent
                if str(current_dir) not in sys.path:
                    sys.path.insert(0, str(current_dir))
                
                from financial_compliance_validator import FinancialComplianceValidator
                validator = FinancialComplianceValidator(
                    require_disclaimers=True,
                    check_guaranteed_returns=True,
                    check_specific_predictions=True,
                    use_llm_verification=False  # Disable for interactive speed
                )
            else:
                print(f"❌ Interactive mode not available for {validator_key}")
                return
            
            # Interactive testing loop
            print("\\n💡 Enter text to validate (type 'quit' to exit, 'examples' for test cases):")
            
            while True:
                try:
                    user_input = input("\\n> ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("👋 Goodbye!")
                        break
                    
                    if user_input.lower() == 'examples':
                        self._show_test_examples(validator_key)
                        continue
                    
                    if not user_input:
                        continue
                    
                    # Validate input
                    print(f"\\n🔍 Validating: '{user_input[:60]}{'...' if len(user_input) > 60 else ''}'")
                    print("-" * 40)
                    
                    result = validator._validate(user_input, {})
                    
                    if hasattr(result, 'error_message'):
                        # Failed validation
                        print("❌ VALIDATION FAILED")
                        print(f"Reason: {result.error_message}")
                        
                        if hasattr(result, 'fix_value') and result.fix_value:
                            print(f"\\n✨ Suggested fix:")
                            print(f"'{result.fix_value}'")
                    else:
                        # Passed validation
                        print("✅ VALIDATION PASSED")
                        print("Content complies with validator requirements")
                
                except KeyboardInterrupt:
                    print("\\n\\n👋 Interrupted by user")
                    break
                except Exception as e:
                    print(f"❌ Error during validation: {e}")
        
        except KeyboardInterrupt:
            print("\\n\\n👋 Cancelled by user")
    
    def _show_test_examples(self, validator_key: str):
        """Show example test cases for a validator."""
        examples = {
            "financial": [
                ("Consider diversifying your portfolio. Not financial advice.", "✅ Should pass"),
                ("I guarantee 50% returns on this investment!", "❌ Should fail - guaranteed returns"),
                ("AAPL will hit $200 next week.", "❌ Should fail - specific prediction"),
                ("You should buy Tesla stock now.", "❌ Should fail - missing disclaimer"),
                ("The weather is nice today.", "✅ Should pass - not financial content")
            ]
        }
        
        if validator_key in examples:
            print("\\n📋 Example test cases:")
            for i, (text, expectation) in enumerate(examples[validator_key], 1):
                print(f"  {i}. '{text}' → {expectation}")
        else:
            print("\\n❌ No examples available for this validator")
    
    def show_architecture_info(self):
        """Show information about custom validator architecture."""
        print("=" * 80)
        print("🏗️  CUSTOM VALIDATOR ARCHITECTURE")
        print("=" * 80)
        print()
        
        print("🔧 VALIDATOR STRUCTURE:")
        print("├── @register_validator decorator")
        print("├── Validator base class inheritance") 
        print("├── _validate() method implementation")
        print("├── PassResult/FailResult return types")
        print("└── Optional fix_value suggestions")
        print()
        
        print("🎯 KEY DESIGN PATTERNS:")
        print("• Multi-stage validation workflows")
        print("• Topic detection → domain-specific rules")
        print("• Pattern matching + LLM integration")
        print("• Fail-safe error handling")
        print("• Automatic content fixing suggestions")
        print()
        
        print("🔌 INTEGRATION OPTIONS:")
        print("• Standalone validator instances")
        print("• Guard.use() method integration")
        print("• RAIL specification embedding")
        print("• Pydantic model validation")
        print("• Streaming validation support")
        print()
        
        print("💡 BEST PRACTICES DEMONSTRATED:")
        print("• Comprehensive error messages")
        print("• Performance-optimized pattern matching")
        print("• External API integration (with fallbacks)")
        print("• Configurable strictness levels")
        print("• Production-ready error handling")


def main():
    """Main entry point for the custom guardrails demo."""
    parser = argparse.ArgumentParser(
        description="Custom Guardrails Demonstrations - Production-Ready Validators"
    )
    parser.add_argument("--validator", "-v", type=str, metavar="NAME",
                       help="Run specific validator demo (e.g., 'financial')")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Launch interactive testing mode")
    parser.add_argument("--list", "-l", action="store_true",
                       help="Show available validators")
    parser.add_argument("--architecture", "-a", action="store_true",
                       help="Show validator architecture information")
    
    args = parser.parse_args()
    
    runner = CustomGuardrailsDemoRunner()
    
    if args.validator:
        runner.run_validator_demo(args.validator)
    elif args.interactive:
        runner.run_interactive_mode()
    elif args.architecture:
        runner.show_architecture_info()
    elif args.list:
        runner.show_menu()
    else:
        runner.show_menu()


if __name__ == "__main__":
    main()