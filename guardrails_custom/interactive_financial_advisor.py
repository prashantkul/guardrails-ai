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
from groq import Groq
from dotenv import load_dotenv

# Add current directory to path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from financial_compliance_validator import FinancialComplianceValidator

load_dotenv()


class InteractiveFinancialAdvisor:
    """Interactive tool for creating compliant financial content."""
    
    # Simple color codes
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
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
        self.groq_model = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # Default to llama3 if not set
        
        # Initialize Groq client
        self.groq_client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        
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
                print(f"\n{self.CYAN}{'=' * 70}{self.END}")
                print(f"{self.BOLD}{self.CYAN}🤖 AI FINANCIAL ADVISOR (with Compliance){self.END}")
                print(f"{self.CYAN}{'=' * 70}{self.END}")
                print(f"\n{self.BOLD}Options:{self.END}")
                print(f"  {self.GREEN}1.{self.END} Ask for financial advice (AI-generated & validated)")
                print(f"  {self.GREEN}2.{self.END} Validate your own financial content")
                print(f"  {self.GREEN}3.{self.END} See compliance tips")
                print(f"  {self.GREEN}4.{self.END} View example compliant phrases")
                print(f"  {self.GREEN}5.{self.END} Test with sample questions")
                print(f"  {self.RED}6.{self.END} Exit")
                
                choice = input(f"\n{self.YELLOW}Select option (1-6): {self.END}").strip()
                
                if choice == "1":
                    self._get_ai_financial_advice()
                elif choice == "2":
                    self._validate_user_content()
                elif choice == "3":
                    self._show_compliance_tips()
                elif choice == "4":
                    self._show_compliant_examples()
                elif choice == "5":
                    self._test_sample_questions()
                elif choice == "6":
                    print("\n👋 Thank you for using the AI Financial Advisor!")
                    break
                else:
                    print(f"{self.RED}❌ Invalid option. Please choose 1-6.{self.END}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{self.YELLOW}👋 Interrupted by user. Goodbye!{self.END}")
                break
            except Exception as e:
                print(f"{self.RED}❌ An error occurred: {e}{self.END}")
    
    def _get_ai_financial_advice(self):
        """Get financial advice from AI and validate it for compliance."""
        print("\n🤖 AI FINANCIAL ADVISOR")
        print("-" * 50)
        print("Ask any financial question (or 'back' to return):")
        print("Examples: 'Should I invest in Tesla?', 'Is gold a good investment?'")
        
        question = input(f"\n{self.YELLOW}❓ Your question: {self.END}").strip()
        if question.lower() == 'back':
            return
        
        if not self.groq_client:
            print(f"\n{self.YELLOW}⚠️  Groq API key not found. Please set GROQ_API_KEY in .env file{self.END}")
            return
        
        print("\n🤔 AI is thinking...")
        
        # Generate AI response using Groq SDK
        prompt = f"""You are a financial advisor. Answer this question: {question}
        
        Provide helpful financial advice but be specific and actionable."""
        
        try:
            completion = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            ai_advice = completion.choices[0].message.content.strip()
            
            print("\n📝 RAW AI RESPONSE:")
            print("-" * 50)
            print(ai_advice)
            print("-" * 50)
            
            # Validate the AI response
            print("\n🔍 Validating for compliance...")
            validation_result = self.validator._validate(ai_advice, {})
            
            if hasattr(validation_result, 'error_message'):
                print(f"\n{self.YELLOW}⚠️  Compliance issues detected: {validation_result.error_message}{self.END}")
                print(f"\n{self.GREEN}✨ FIXED & COMPLIANT VERSION:{self.END}")
                print(f"{self.GREEN}{'=' * 50}{self.END}")
                compliant_advice = validation_result.fix_value if validation_result.fix_value else self._rule_based_enhancement(ai_advice)
                print(f"{self.BOLD}{compliant_advice}{self.END}")
                print(f"{self.GREEN}{'=' * 50}{self.END}")
                
                # Show what changed
                print("\n📊 What was changed:")
                if "guaranteed" in ai_advice.lower() and "guaranteed" not in compliant_advice.lower():
                    print("  • Removed guaranteed return language")
                if "not financial advice" not in ai_advice.lower() and "not financial advice" in compliant_advice.lower():
                    print("  • Added required disclaimer")
                if "will" in ai_advice.lower() and ("might" in compliant_advice.lower() or "could" in compliant_advice.lower()):
                    print("  • Softened predictions with uncertainty language")
                
            else:
                print(f"\n{self.GREEN}✅ AI response is already compliant!{self.END}")
                print(f"\n{self.GREEN}📝 COMPLIANT ADVICE:{self.END}")
                print(f"{self.GREEN}{'=' * 50}{self.END}")
                print(f"{self.BOLD}{ai_advice}{self.END}")
                print(f"{self.GREEN}{'=' * 50}{self.END}")
            
            # Save the advice automatically
            final_advice = compliant_advice if hasattr(validation_result, 'error_message') else ai_advice
            
            # Ask if user wants to save
            save_choice = input("\n💾 Would you like to save this advice to a file? (y/n): ").strip().lower()
            if save_choice == 'y':
                self._save_to_file(f"Question: {question}\n\nAdvice:\n{final_advice}")
            
            # Return to main menu
            print("\n↩️  Returning to main menu...")
                
        except Exception as e:
            print(f"{self.RED}❌ Error getting AI advice: {e}{self.END}")
    
    def _show_welcome(self):
        """Display welcome message and introduction."""
        print(f"{self.CYAN}{'=' * 70}{self.END}")
        print(f"{self.BOLD}{self.CYAN}🏦 AI FINANCIAL ADVISOR WITH COMPLIANCE VALIDATION{self.END}")
        print(f"{self.CYAN}{'=' * 70}{self.END}")
        print(f"\n{self.BOLD}Welcome! This tool provides AI-generated financial advice that is:{self.END}")
        print(f"{self.GREEN}✅ Automatically validated for regulatory compliance{self.END}")
        print(f"{self.GREEN}✅ Enhanced with required disclaimers and risk warnings{self.END}")
        print(f"{self.GREEN}✅ Free from prohibited guarantee language{self.END}")
        print(f"{self.GREEN}✅ Properly hedged with uncertainty language{self.END}")
        print(f"\n{self.YELLOW}💡 How it works:{self.END}")
        print("   1. You ask a financial question")
        print("   2. AI generates advice")
        print("   3. Validator ensures compliance")
        print("   4. You receive safe, compliant advice")
    
    def _validate_user_content(self):
        """Validate user-provided financial content."""
        print("\n📋 CONTENT VALIDATION")
        print("-" * 50)
        print("Enter your financial content (or 'back' to return):")
        
        content = input(f"{self.YELLOW}> {self.END}").strip()
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
        
        content = input(f"{self.YELLOW}> {self.END}").strip()
        if content.lower() == 'back':
            return
        
        self._enhance_content_with_llm(content)
    
    def _enhance_content_with_llm(self, content: str, already_compliant: bool = False):
        """Use LLM to enhance content with proper compliance elements."""
        if not self.groq_client:
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
            completion = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            enhanced_content = completion.choices[0].message.content.strip()
            
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
            
            # Ask if user wants to save
            save_choice = input("\n💾 Would you like to save this enhanced content to a file? (y/n): ").strip().lower()
            if save_choice == 'y':
                self._save_to_file(enhanced_content)
            
            # Return to main menu
            print("\n↩️  Returning to main menu...")
                
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            print("Using rule-based enhancement instead...")
            enhanced = self._rule_based_enhancement(content)
            print("\n📝 Enhanced content (rule-based):")
            print(enhanced)
    
    def _rule_based_enhancement(self, content: str) -> str:
        """Apply rule-based enhancements for compliance."""
        enhanced = content
        
        # Soften guaranteed language first
        enhanced = re.sub(r'\bguarantee[sd]?\b', 'potentially', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bcannot lose\b', 'may have lower risk', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\brisk[- ]free\b', 'lower risk', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill definitely\b', 'might', enhanced, flags=re.IGNORECASE)
        
        # Soften predictions
        enhanced = re.sub(r'\bwill hit\b', 'could potentially reach', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill be worth\b', 'might be valued at', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill double\b', 'could potentially increase', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill\b', 'might', enhanced, flags=re.IGNORECASE)
        
        # Check if it needs disclaimers - check both original and enhanced content
        has_financial_terms = any(
            keyword in enhanced.lower() 
            for keyword in ['invest', 'stock', 'profit', 'money', 'buy', 'sell', 'trading', 'portfolio']
        )
        
        has_disclaimer = any(
            disclaimer in enhanced.lower() 
            for disclaimer in self.validator.disclaimer_keywords
        )
        
        # Always add disclaimer if it's financial content without one
        if has_financial_terms and not has_disclaimer:
            enhanced += "\n\nDisclaimer: This is not financial advice. Please consult with a qualified financial professional before making any investment decisions. Past performance does not guarantee future results."
        
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
    
    def _test_sample_questions(self):
        """Test with sample financial questions."""
        print("\n🧪 SAMPLE QUESTIONS & AI RESPONSES")
        print("=" * 50)
        
        sample_questions = [
            "Should I invest all my savings in Tesla stock?",
            "What's a guaranteed way to double my money?",
            "Is cryptocurrency a good investment for retirement?",
            "Should I buy or rent a house in this market?",
            "How can I get rich quickly with stocks?"
        ]
        
        print("\nExample questions you can ask:")
        for i, question in enumerate(sample_questions, 1):
            print(f"{i}. {question}")
        
        print("\n💡 These questions will generate AI advice that gets validated for compliance.")
        print("   Try option 1 to ask your own questions!")
        
        # Show a demo of what happens
        print("\n" + "-" * 50)
        print("DEMO: What happens when you ask a question:")
        print("-" * 50)
        print("Question: 'Should I buy Bitcoin?'")
        print("\n1️⃣ AI might say: 'Bitcoin will definitely double in value next month!'")
        print("2️⃣ Validator detects: Specific prediction without uncertainty")  
        print("3️⃣ Fixed version: 'Bitcoin could potentially see growth, though cryptocurrency")
        print("   is highly volatile. This is not financial advice. Consult a professional.'")
        print("\n✅ You receive the compliant version!")
    
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