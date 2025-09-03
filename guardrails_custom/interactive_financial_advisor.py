#!/usr/bin/env python3
"""
Interactive Financial Advisor Compliance Tool
=============================================

An interactive tool that helps users write compliant financial content by:
1. Validating their input against regulatory requirements
2. Using LLM to enhance non-compliant content with proper disclaimers
3. Educating users about financial compliance best practices

This demonstrates real-world application of the Financial Compliance Validator.
"""

import os
import sys
import re
from pathlib import Path
from typing import Optional, Tuple
import requests
from dotenv import load_dotenv

# Add current directory to path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from financial_compliance_validator import FinancialComplianceValidator

load_dotenv()


class InteractiveFinancialAdvisor:
    """Interactive tool for creating compliant financial content."""
    
    def __init__(self):
        """Initialize the interactive advisor."""
        self.validator = FinancialComplianceValidator(
            require_disclaimers=True,
            check_guaranteed_returns=True,
            check_specific_predictions=True,
            check_unlicensed_advice=True,
            use_llm_verification=False  # We'll use LLM for enhancement instead
        )
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Educational compliance tips
        self.compliance_tips = [
            "Always include disclaimers like 'Not financial advice'",
            "Avoid guaranteed return language (e.g., 'guaranteed profits')",
            "Use uncertainty language for predictions (e.g., 'might', 'could')",
            "Mention consulting professionals for serious decisions",
            "Avoid overly specific price/date predictions",
            "Include risk warnings where appropriate"
        ]
        
        # Example compliant phrases
        self.compliant_examples = {
            "disclaimer": "This is not financial advice. Please consult a qualified financial advisor.",
            "risk_warning": "All investments carry risk. Past performance doesn't guarantee future results.",
            "uncertainty": ["may potentially", "could possibly", "might consider"],
            "professional": "consult with a licensed financial professional",
            "educational": "for educational purposes only"
        }
    
    def run(self):
        """Run the interactive financial advisor interface."""
        self._show_welcome()
        
        while True:
            try:
                print("\n" + "=" * 70)
                print("📝 FINANCIAL CONTENT VALIDATOR")
                print("=" * 70)
                print("\nOptions:")
                print("  1. Validate your financial content")
                print("  2. Get AI help to make content compliant")
                print("  3. See compliance tips")
                print("  4. View example compliant phrases")
                print("  5. Test with sample content")
                print("  6. Exit")
                
                choice = input("\nSelect option (1-6): ").strip()
                
                if choice == "1":
                    self._validate_user_content()
                elif choice == "2":
                    self._enhance_with_ai()
                elif choice == "3":
                    self._show_compliance_tips()
                elif choice == "4":
                    self._show_compliant_examples()
                elif choice == "5":
                    self._test_samples()
                elif choice == "6":
                    print("\n👋 Thank you for using the Financial Compliance Tool!")
                    break
                else:
                    print("❌ Invalid option. Please choose 1-6.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
    
    def _show_welcome(self):
        """Display welcome message and introduction."""
        print("=" * 70)
        print("🏦 INTERACTIVE FINANCIAL ADVISOR COMPLIANCE TOOL")
        print("=" * 70)
        print("\nWelcome! This tool helps you create compliant financial content that:")
        print("✅ Meets regulatory requirements (SEC/FINRA guidelines)")
        print("✅ Includes proper disclaimers and risk warnings")
        print("✅ Avoids prohibited language (guaranteed returns, etc.)")
        print("✅ Uses appropriate uncertainty language for predictions")
        print("\n💡 Tip: Always remember - financial content requires extra care!")
    
    def _validate_user_content(self):
        """Validate user-provided financial content."""
        print("\n📋 CONTENT VALIDATION")
        print("-" * 50)
        print("Enter your financial content (or 'back' to return):")
        
        content = self._get_multiline_input()
        if content.lower() == 'back':
            return
        
        print("\n🔍 Validating content...")
        result = self.validator._validate(content, {})
        
        if hasattr(result, 'error_message'):
            # Failed validation
            print("\n❌ VALIDATION FAILED")
            print(f"Issues found: {result.error_message}")
            
            if hasattr(result, 'fix_value') and result.fix_value:
                print("\n✨ Quick fix suggestion:")
                print(f"'{result.fix_value}'")
            
            print("\n💡 Would you like me to enhance this with AI? (y/n)")
            if input().strip().lower() == 'y':
                self._enhance_content_with_llm(content)
        else:
            # Passed validation
            print("\n✅ VALIDATION PASSED")
            print("Your content meets financial compliance requirements!")
            
            # Still offer enhancement
            print("\n💭 Would you like to enhance it further with AI? (y/n)")
            if input().strip().lower() == 'y':
                self._enhance_content_with_llm(content, already_compliant=True)
    
    def _enhance_with_ai(self):
        """Get user content and enhance it with AI for compliance."""
        print("\n🤖 AI-POWERED COMPLIANCE ENHANCEMENT")
        print("-" * 50)
        print("Enter your financial content to enhance (or 'back' to return):")
        
        content = self._get_multiline_input()
        if content.lower() == 'back':
            return
        
        self._enhance_content_with_llm(content)
    
    def _enhance_content_with_llm(self, content: str, already_compliant: bool = False):
        """Use LLM to enhance content with proper compliance elements."""
        if not self.groq_api_key:
            print("\n⚠️  Groq API key not found. Using rule-based enhancement instead.")
            enhanced = self._rule_based_enhancement(content)
            print("\n📝 Enhanced content (rule-based):")
            print("-" * 50)
            print(enhanced)
            return
        
        print("\n🔄 Enhancing with AI...")
        
        if already_compliant:
            prompt = f"""
            The following financial content is already compliant but could be enhanced.
            Add any additional risk warnings, educational context, or professional language
            that would make it even better while maintaining the original message:

            "{content}"

            Enhance it to be more professional and comprehensive while keeping it concise.
            """
        else:
            prompt = f"""
            Transform the following financial content to be fully compliant with SEC/FINRA regulations:

            "{content}"

            Requirements:
            1. Add appropriate disclaimers (e.g., "Not financial advice")
            2. Replace any guaranteed return language with uncertainty terms
            3. Soften specific predictions with words like "might", "could", "potentially"
            4. Include risk warnings where appropriate
            5. Suggest consulting professionals for serious decisions
            6. Maintain the core message while ensuring compliance

            Provide the enhanced version that is both compliant and maintains the intended message.
            """
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                enhanced_content = result["choices"][0]["message"]["content"].strip()
                
                print("\n✨ AI-ENHANCED COMPLIANT VERSION:")
                print("=" * 50)
                print(enhanced_content)
                print("=" * 50)
                
                # Validate the enhanced version
                print("\n🔍 Validating enhanced content...")
                validation_result = self.validator._validate(enhanced_content, {})
                
                if hasattr(validation_result, 'error_message'):
                    print("⚠️  Enhanced content still has issues. Applying additional fixes...")
                    # Apply additional rule-based fixes
                    enhanced_content = self._rule_based_enhancement(enhanced_content)
                    print("\n📝 Final enhanced version:")
                    print(enhanced_content)
                else:
                    print("✅ Enhanced content is fully compliant!")
                
                # Offer to copy or save
                print("\n💾 Options:")
                print("  1. Copy to clipboard (if supported)")
                print("  2. Save to file")
                print("  3. Continue")
                
                save_choice = input("\nSelect option (1-3): ").strip()
                if save_choice == "2":
                    self._save_to_file(enhanced_content)
                elif save_choice == "1":
                    print("📋 Copy the text above manually (clipboard integration varies by system)")
                
            else:
                print(f"❌ API error: {response.status_code}")
                print("Using rule-based enhancement instead...")
                enhanced = self._rule_based_enhancement(content)
                print("\n📝 Enhanced content (rule-based):")
                print(enhanced)
                
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            print("Using rule-based enhancement instead...")
            enhanced = self._rule_based_enhancement(content)
            print("\n📝 Enhanced content (rule-based):")
            print(enhanced)
    
    def _rule_based_enhancement(self, content: str) -> str:
        """Apply rule-based enhancements for compliance."""
        enhanced = content
        
        # Check if it needs disclaimers
        has_advice = any(
            re.search(pattern, content.lower()) 
            for pattern in self.validator.advice_indicators
        )
        
        has_disclaimer = any(
            disclaimer in content.lower() 
            for disclaimer in self.validator.disclaimer_keywords
        )
        
        # Add disclaimer if missing and has advice
        if has_advice and not has_disclaimer:
            enhanced += "\n\nDisclaimer: This is not financial advice. Please consult with a qualified financial professional before making any investment decisions. Past performance does not guarantee future results."
        
        # Soften guaranteed language
        enhanced = re.sub(r'\bguarantee[sd]?\b', 'potentially', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bcannot lose\b', 'may have lower risk', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\brisk[- ]free\b', 'lower risk', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill definitely\b', 'might', enhanced, flags=re.IGNORECASE)
        
        # Soften predictions
        enhanced = re.sub(r'\bwill hit\b', 'could potentially reach', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill be worth\b', 'might be valued at', enhanced, flags=re.IGNORECASE)
        
        return enhanced
    
    def _show_compliance_tips(self):
        """Display compliance tips."""
        print("\n📚 FINANCIAL COMPLIANCE TIPS")
        print("=" * 50)
        for i, tip in enumerate(self.compliance_tips, 1):
            print(f"{i}. {tip}")
        
        print("\n🎯 Key Principles:")
        print("• Transparency: Be clear about risks and uncertainties")
        print("• Humility: Avoid absolute statements about future performance")
        print("• Education: Focus on informing rather than directing")
        print("• Protection: Always encourage professional consultation")
    
    def _show_compliant_examples(self):
        """Show examples of compliant phrases."""
        print("\n✅ COMPLIANT PHRASE EXAMPLES")
        print("=" * 50)
        
        print("\n📌 Disclaimers:")
        print(f"  • '{self.compliant_examples['disclaimer']}'")
        print(f"  • '{self.compliant_examples['risk_warning']}'")
        print(f"  • '{self.compliant_examples['educational']}'")
        
        print("\n📌 Uncertainty Language:")
        print(f"  • Examples: {', '.join(self.compliant_examples['uncertainty'])}")
        print("  • Instead of 'will' → use 'might', 'could', 'may'")
        print("  • Instead of 'guaranteed' → use 'potential', 'possible'")
        print("  • Instead of 'definitely' → use 'likely', 'probably'")
        
        print("\n📌 Professional References:")
        print(f"  • '{self.compliant_examples['professional']}'")
        print("  • 'Seek advice from a licensed investment advisor'")
        print("  • 'Discuss with your financial planner'")
    
    def _test_samples(self):
        """Test with sample content."""
        print("\n🧪 SAMPLE CONTENT TESTS")
        print("=" * 50)
        
        samples = [
            ("Buy AAPL stock now - guaranteed 50% returns!", "Non-compliant: Guaranteed returns + direct advice"),
            ("Consider diversifying your portfolio. Not financial advice.", "Compliant: Has disclaimer"),
            ("Tesla will hit $500 next month!", "Non-compliant: Specific prediction"),
            ("Market analysis suggests potential growth opportunities.", "Compliant: Uses uncertainty language"),
            ("This risk-free investment cannot lose money.", "Non-compliant: Risk-free claims")
        ]
        
        for i, (content, description) in enumerate(samples, 1):
            print(f"\n{i}. {description}")
            print(f"   Content: '{content}'")
            
            result = self.validator._validate(content, {})
            if hasattr(result, 'error_message'):
                print(f"   Status: ❌ Failed - {result.error_message}")
            else:
                print(f"   Status: ✅ Passed")
        
        print("\n💡 Try option 2 to see how AI can fix non-compliant content!")
    
    def _get_multiline_input(self) -> str:
        """Get multiline input from user."""
        print("(Enter your text, then press Enter twice to submit)")
        lines = []
        empty_line_count = 0
        
        while empty_line_count < 1:
            line = input()
            if line == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
                lines.append(line)
        
        return "\n".join(lines)
    
    def _save_to_file(self, content: str):
        """Save content to a file."""
        filename = input("Enter filename (default: compliant_content.txt): ").strip()
        if not filename:
            filename = "compliant_content.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")


def main():
    """Main entry point."""
    print("\n🚀 Starting Interactive Financial Advisor Compliance Tool...")
    advisor = InteractiveFinancialAdvisor()
    advisor.run()


if __name__ == "__main__":
    main()