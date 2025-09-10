#!/usr/bin/env python3
"""
Gradio Financial Advisor with Gemini & Guardrails Integration
============================================================

A web-based financial advisor application built with Gradio that:
1. Uses Google Gemini for AI-powered financial advice generation
2. Validates user prompts before sending to LLM (prompt guardrails)
3. Validates AI responses after generation (response guardrails)  
4. Provides a clean, user-friendly web interface
5. Demonstrates comprehensive AI safety in financial applications

This combines the power of Gradio's interface with the existing 
financial compliance validator for a production-ready solution.
"""

import os
import sys
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import gradio as gr
from dotenv import load_dotenv
import google.generativeai as genai

# Add current directory to path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import existing guardrails
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

# Import prompt management
from financial_advisor_prompts import FinancialAdvisorPrompts, PromptVersion

# Import spaCy NER for enhanced analysis
try:
    from spacy_financial_ner import FinancialRiskNER
    SPACY_NER_AVAILABLE = True
except ImportError:
    SPACY_NER_AVAILABLE = False

# Import Jinja2 template manager for clean HTML/CSS separation
try:
    from jinja_template_manager import template_manager
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    template_manager = None

# Load environment variables
load_dotenv()


class GradioFinancialAdvisor:
    """Gradio-based Financial Advisor with Gemini and Guardrails."""

    def __init__(self):
        """Initialize the Gradio Financial Advisor."""

        # Initialize Gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None

        # Initialize financial compliance validators
        # Prompt validator (more permissive for user input)
        self.prompt_validator = FinancialComplianceValidator(
            require_disclaimers=False,  # Users don't need disclaimers in questions
            check_guaranteed_returns=True,  # Check for problematic language
            check_specific_predictions=True,  # Detect prediction requests
            check_unlicensed_advice=False,  # Users aren't giving advice
            use_llm_verification=False,  # Keep it fast for prompt validation
            strict_compliance=True,  # Make it more sensitive for prompts
            fast_mode=True  # Optimize for speed with pattern-first approach
        )

        # Response validator (strict for AI outputs)
        self.response_validator = FinancialComplianceValidator(
            require_disclaimers=True,
            check_guaranteed_returns=True,
            check_specific_predictions=True,
            check_unlicensed_advice=True,
            use_llm_verification=False,  # Use rule-based for speed
            strict_compliance=True,
            fast_mode=True  # Optimize for speed with hybrid approach
        )

        # Track conversation history
        self.conversation_history = []
        
        # Current prompt version (default to compliant)
        self.current_prompt_version = PromptVersion.COMPLIANT
        
        # Store the latest compliance analysis for the dedicated page
        self.latest_compliance_analysis = ""
        self.latest_validation_info = ""
        
        # Initialize enhanced spaCy NER if available
        self.spacy_ner = None
        if SPACY_NER_AVAILABLE:
            try:
                self.spacy_ner = FinancialRiskNER()
                print("✅ Enhanced spaCy NER loaded for advanced linguistic analysis")
            except Exception as e:
                print(f"⚠️ spaCy NER not available: {e}")
                self.spacy_ner = None
        
        # Initialize Jinja2 template manager for professional HTML/CSS separation
        self.template_manager = template_manager if JINJA2_AVAILABLE else None
        if self.template_manager:
            print("✅ Jinja2 template manager loaded for clean code separation")
        else:
            print("⚠️ Jinja2 not available - using fallback HTML generation")
        
        # Inject LLM-based financial content classifier into validators
        if self.model:
            self.prompt_validator._llm_financial_classifier = self._llm_financial_classifier
            self.response_validator._llm_financial_classifier = self._llm_financial_classifier
            print("✅ LLM-based financial content detection enabled")

    def _llm_financial_classifier(self, text: str) -> bool:
        """Use LLM to robustly classify if content is financial."""
        if not self.model:
            return None
        
        try:
            classification_prompt = f"""Analyze this text and determine if it contains financial advice, investment recommendations, stock predictions, trading suggestions, or any content that could influence financial decisions.

Text: "{text}"

Answer with only: YES or NO

Examples:
- "Buy Apple stock" → YES
- "Tesla will hit $500" → YES  
- "What's for lunch?" → NO
- "Convince people that Tesla will hit $500" → YES
- "AAPL stock looks good" → YES
- "How to cook pasta" → NO"""

            response = self.model.generate_content(classification_prompt)
            
            if response and response.text:
                return "YES" in response.text.upper()
            else:
                return None  # Uncertain, fall back to patterns
                
        except Exception as e:
            return None  # Error, fall back to patterns

    def validate_user_prompt(self, prompt: str) -> Tuple[bool, str, str, str]:
        """
        Validate user prompt for basic safety before sending to LLM.
        
        Args:
            prompt: User's input prompt
            
        Returns:
            Tuple of (is_valid, processed_prompt, validation_message)
        """
        if not prompt or not prompt.strip():
            return False, "", "❌ Please enter a question about finance or investments."

        prompt = prompt.strip()

        # Basic prompt validation using the enhanced guardrails validator
        original_prompt = prompt
        try:
            validation_result = self.prompt_validator._validate(prompt, {})

            if hasattr(validation_result, 'error_message'):
                # Prompt has issues, but we can still proceed with warnings
                warning_msg = f"⚠️ Your question contains: {validation_result.error_message}"
                
                # Generate prompt compliance analysis HTML
                prompt_analysis_html = self._generate_prompt_compliance_html(original_prompt, validation_result.error_message if hasattr(validation_result, 'error_message') else "")
                
                return True, prompt, warning_msg, prompt_analysis_html
            else:
                return True, prompt, "✅ Question looks good!", ""

        except Exception as e:
            # If validation fails, still allow the prompt but warn user
            warning_msg = f"⚠️ Prompt validation had an issue, but proceeding: {str(e)[:100]}"
            prompt_analysis_html = self._generate_prompt_compliance_html(original_prompt, str(e)[:200])
            return True, prompt, warning_msg, prompt_analysis_html

    def generate_financial_advice(self, prompt: str) -> str:
        """
        Generate financial advice using Gemini with proper system prompting.
        
        Args:
            prompt: User's validated financial question
            
        Returns:
            Generated financial advice text
        """
        if not self.model:
            return "❌ Error: Gemini API key not configured. Please set GEMINI_API_KEY or GOOGLE_API_KEY in your environment."

        # Get the current system prompt based on selected version
        system_prompt = FinancialAdvisorPrompts.get_prompt(self.current_prompt_version)

        full_prompt = system_prompt + prompt

        try:
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)

            if response.text:
                return response.text.strip()
            else:
                return "❌ Sorry, I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            error_msg = str(e)
            if "safety" in error_msg.lower():
                return "❌ The question was blocked by safety filters. Please try asking in a different way."
            else:
                return f"❌ Error generating response: {error_msg[:200]}..."

    def validate_ai_response(self, response: str) -> Tuple[str, str, bool, str]:
        """
        Validate AI-generated response for financial compliance.
        
        Args:
            response: AI-generated financial advice
            
        Returns:
            Tuple of (final_response, validation_status, needs_human_review, comparison_html)
        """
        if not response or response.startswith("❌"):
            return response, "⚠️ Response validation skipped due to generation error", False, ""

        try:
            # Store original for comparison
            original_response = response
            
            # Validate the response
            validation_result = self.response_validator._validate(response, {})

            if hasattr(validation_result, 'error_message'):
                # Response failed validation - get the compliant version
                compliance_issues = validation_result.error_message
                compliant_response = validation_result.fix_value if hasattr(validation_result, 'fix_value') and validation_result.fix_value else None

                if compliant_response and compliant_response != response:
                    # Use the guardrails-provided compliant version
                    validation_status = f"🔧 Response enhanced for compliance\n📋 Issues addressed: {compliance_issues}"
                    comparison_html = self._generate_compliance_diff_html(original_response, compliant_response)
                    return compliant_response, validation_status, False, comparison_html
                else:
                    # Fallback to rule-based enhancement
                    enhanced_response = self._rule_based_compliance_fix(response)
                    validation_status = f"⚠️ Applied rule-based compliance fixes\n📋 Issues: {compliance_issues}"
                    comparison_html = self._generate_compliance_diff_html(original_response, enhanced_response)
                    return enhanced_response, validation_status, True, comparison_html
            else:
                # Response passed validation
                validation_status = "✅ Response meets all financial compliance requirements"
                return response, validation_status, False, ""

        except Exception as e:
            # Validation error - apply conservative fixes
            enhanced_response = self._rule_based_compliance_fix(response)
            validation_status = f"⚠️ Validation error, applied safety enhancements: {str(e)[:100]}"
            comparison_html = self._generate_compliance_diff_html(response, enhanced_response)
            return enhanced_response, validation_status, True, comparison_html

    def _rule_based_compliance_fix(self, text: str) -> str:
        """Apply rule-based compliance fixes to AI response."""
        enhanced = text

        # Fix guaranteed language
        enhanced = re.sub(r'\bguarantee[sd]?\b', 'potentially offer', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\brisk[- ]free\b', 'lower risk', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bcannot lose\b', 'may have lower risk of loss', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill definitely\b', 'might', enhanced, flags=re.IGNORECASE)

        # Soften predictions
        enhanced = re.sub(r'\bwill hit\b', 'could potentially reach', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill be worth\b', 'might be valued at', enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r'\bwill increase\b', 'could potentially increase', enhanced, flags=re.IGNORECASE)

        # Check if disclaimer is needed
        has_financial_terms = any(
            keyword in enhanced.lower() 
            for keyword in ['invest', 'stock', 'buy', 'sell', 'trading', 'portfolio', 'profit', 'return']
        )

        has_disclaimer = any(
            disclaimer in enhanced.lower() 
            for disclaimer in ['not financial advice', 'not investment advice', 'consult', 'professional']
        )

        # Add disclaimer if needed
        if has_financial_terms and not has_disclaimer:
            enhanced += "\n\n**Important Disclaimer**: This information is for educational purposes only and is not personalized financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results, and all investments carry risk."

        return enhanced
    
    def _generate_compliance_diff_html(self, original: str, compliant: str) -> str:
        """
        Generate HTML showing the differences between original and compliant versions.
        
        Args:
            original: Original AI response
            compliant: Compliance-enhanced version
            
        Returns:
            HTML string with highlighted differences
        """
        # Check if there are significant changes by comparing content
        if original.strip() == compliant.strip():
            return self.template_manager.render_compliance_analysis(
                original_content=original,
                compliant_content=original,  # Same content
                title="Response Analysis",
                summary="No significant changes were needed for compliance.",
                mode=self.current_prompt_version.value.title()
            )
        
        # Use Jinja2 template for professional rendering
        return self.template_manager.render_compliance_analysis(
            original_content=original,
            compliant_content=compliant,
            mode=self.current_prompt_version.value.title(),
            analysis_type="Response Enhancement"
        )
    
    
    

    def _generate_prompt_compliance_html(self, original_prompt: str, error_message: str) -> str:
        """
        Generate HTML showing prompt compliance issues and analysis.
        
        Args:
            original_prompt: The user's original question
            error_message: The validation error message
            
        Returns:
            HTML string with highlighted prompt issues and analysis
        """
        # Enhanced spaCy analysis if available
        spacy_entities = []
        spacy_summary = ""
        if self.spacy_ner:
            try:
                entities, analysis = self.spacy_ner.analyze_text(original_prompt)
                spacy_entities = entities
                if entities:
                    spacy_summary = f"🔍 **Enhanced NLP Analysis**: {analysis['overall_risk'].upper()} risk ({len(entities)} entities detected)"
            except Exception as e:
                spacy_summary = f"⚠️ Advanced analysis unavailable: {str(e)[:50]}"
        
        # Analyze problematic words for template
        problematic_words = []
        detected_entities = []
        
        if spacy_entities:
            for entity in spacy_entities:
                problematic_words.append((entity.text, entity.description))
                detected_entities.append({
                    'text': entity.text,
                    'type': entity.label,  # Fixed: use .label instead of .label_
                    'description': entity.description,
                    'color': '#ff6b6b' if entity.risk_level == 'high' else '#ffa726' if entity.risk_level == 'medium' else '#ffcc02'
                })
        
        # Generate safer version
        safer_prompt = self._generate_safer_prompt_version(original_prompt)
        
        # Analyze issues for display
        issues_found = self._analyze_prompt_issues(problematic_words, error_message)
        
        # Use Jinja2 template for professional rendering
        return self.template_manager.render_prompt_analysis(
            original_prompt=original_prompt,
            safer_prompt=safer_prompt,
            error_message=error_message,
            issues_found=issues_found,
            detected_entities=detected_entities,
            spacy_analysis=spacy_summary
        )

    def _generate_safer_prompt_version(self, original_prompt: str) -> str:
        """Generate a safer, more compliant version using LLM rewriting."""
        if not self.model:
            return original_prompt
        
        try:
            # Use the LLM to intelligently rewrite the prompt
            rewrite_prompt = f"""Rewrite this financial question to be compliant and educational:

Original question: "{original_prompt}"

Requirements:
- Remove words like "guaranteed", "risk-free", "secret", "insider"
- Use educational language like "What factors should I consider..."
- Focus on learning, not specific advice
- Keep it natural and conversational
- Make it about 1-2 sentences

Example:
Original: "What's a guaranteed risk-free investment?"
Rewritten: "What factors should I consider when evaluating lower-risk investment options?"

Rewrite the original question following these guidelines:"""

            response = self.model.generate_content(rewrite_prompt)
            
            if response and response.text:
                # Return the LLM response as-is, just stripped of whitespace
                return response.text.strip()
            else:
                return original_prompt
                
        except Exception as e:
            return original_prompt

    def _analyze_prompt_issues(self, problematic_words: list, error_message: str) -> str:
        """Analyze specific issues found in the prompt."""
        issues = []
        
        if problematic_words:
            word_issues = {}
            for word, issue_type in problematic_words:
                if issue_type not in word_issues:
                    word_issues[issue_type] = []
                word_issues[issue_type].append(f"'{word}'")
            
            for issue_type, words in word_issues.items():
                issues.append(f"🔴 <strong>{issue_type.title()}:</strong> {', '.join(words[:3])}")  # Show max 3 examples
        
        # Add general guidance based on error message
        if 'guarantee' in error_message.lower():
            issues.append("📚 <strong>Guidance:</strong> Avoid words that promise certain outcomes")
        if 'risk' in error_message.lower():
            issues.append("📚 <strong>Guidance:</strong> All investments carry some level of risk")
        if 'advice' in error_message.lower():
            issues.append("📚 <strong>Guidance:</strong> Request information rather than specific advice")
        
        if not issues:
            issues.append("⚠️ General compliance concerns detected - using safer processing")
        
        return "<br>".join([f"• {issue}" for issue in issues])

    def set_prompt_version(self, version_name: str):
        """
        Set the current prompt version.
        
        Args:
            version_name: Name of the prompt version to use
        """
        try:
            self.current_prompt_version = PromptVersion(version_name.lower())
            return f"✅ Switched to {version_name.upper()} prompt mode"
        except ValueError:
            return f"❌ Unknown prompt version: {version_name}"
    
    def get_current_prompt_info(self) -> str:
        """Get information about the current prompt version."""
        characteristics = FinancialAdvisorPrompts.get_prompt_characteristics()
        current_chars = characteristics.get(self.current_prompt_version.value, {})
        
        info = f"**Current Mode**: {self.current_prompt_version.value.upper()}\n"
        info += f"**Compliance Level**: {current_chars.get('compliance_level', 'Unknown')}\n"
        info += f"**Use Case**: {current_chars.get('use_case', 'Unknown')}\n"
        info += f"**Risk Level**: {current_chars.get('risk_level', 'Unknown')}"
        
        return info

    def process_question(self, user_question: str, history: list) -> Tuple[list, str, str]:
        """
        Main processing function for Gradio interface.
        
        Args:
            user_question: User's financial question
            history: Chat history from Gradio
            
        Returns:
            Tuple of (updated_history, empty_string_for_input_clear, validation_info)
        """
        import time
        
        pipeline_start = time.perf_counter()
        print(f"\n🚀 NEW REQUEST: '{user_question[:60]}{'...' if len(user_question) > 60 else ''}'")
        
        if not user_question:
            return history, "", "Please enter a question about finance or investments."

        # Step 1: Validate user prompt
        step1_start = time.perf_counter()
        print(f"📥 STEP 1: Validating user prompt...")
        is_valid, processed_prompt, prompt_validation, prompt_analysis_html = self.validate_user_prompt(user_question)
        step1_time = time.perf_counter() - step1_start
        
        if not is_valid:
            total_time = time.perf_counter() - pipeline_start
            print(f"🚫 PIPELINE STOPPED: Prompt blocked ({step1_time:.6f}s validation, {total_time:.6f}s total)")
            history.append((user_question, f"❌ {prompt_validation}"))
            # Store prompt analysis even for invalid prompts
            if prompt_analysis_html:
                self.latest_compliance_analysis = prompt_analysis_html
            return history, "", prompt_validation

        print(f"✅ STEP 1 COMPLETED: Prompt validated ({step1_time:.6f}s)")

        # Step 2: Generate AI response
        step2_start = time.perf_counter()
        print(f"🤖 STEP 2: Generating AI response...")
        ai_response = self.generate_financial_advice(processed_prompt)
        step2_time = time.perf_counter() - step2_start
        print(f"✅ STEP 2 COMPLETED: Response generated ({step2_time:.6f}s, {len(ai_response)} chars)")

        # Step 3: Validate AI response
        step3_start = time.perf_counter()
        print(f"🔍 STEP 3: Validating AI response...")
        final_response, response_validation, needs_review, comparison_html = self.validate_ai_response(ai_response)
        step3_time = time.perf_counter() - step3_start
        print(f"✅ STEP 3 COMPLETED: Response validated ({step3_time:.6f}s)")

        # Step 4: Update conversation history
        total_time = time.perf_counter() - pipeline_start
        print(f"📈 PIPELINE SUMMARY:")
        print(f"   Step 1 (Prompt validation): {step1_time:.6f}s ({step1_time/total_time*100:.1f}%)")
        print(f"   Step 2 (AI generation): {step2_time:.6f}s ({step2_time/total_time*100:.1f}%)")
        print(f"   Step 3 (Response validation): {step3_time:.6f}s ({step3_time/total_time*100:.1f}%)")
        print(f"   🎯 TOTAL PIPELINE: {total_time:.6f}s")
        
        history.append((user_question, final_response))

        # Step 5: Store latest analysis for the dedicated page
        combined_analysis = ""
        
        # Add prompt analysis if there were issues
        if prompt_analysis_html:
            combined_analysis += prompt_analysis_html
        
        # Add response analysis if there were issues
        if comparison_html:
            if combined_analysis:  # If we already have prompt analysis
                combined_analysis += "<div style='height: 30px;'></div>"  # Add spacing
            combined_analysis += comparison_html
        
        # Store the combined analysis or fallback message
        self.latest_compliance_analysis = combined_analysis if combined_analysis else "<div style='padding: 20px; text-align: center; color: #6c757d;'>✅ Latest interaction was already compliant - no analysis needed.</div>"
        
        # Step 6: Prepare validation info for display
        validation_info = f"**Prompt Check**: {prompt_validation}\n\n**Response Check**: {response_validation}"

        if needs_review:
            validation_info += "\n\n⚠️ **Human Review Recommended**: This response was automatically enhanced but may benefit from expert review."
        
        # Add link to detailed analysis if available
        if comparison_html or prompt_analysis_html:
            validation_info += "\n\n🔍 **View detailed compliance analysis in the 'Compliance Analysis' tab** →"

        self.latest_validation_info = validation_info
        return history, "", validation_info

    def create_chat_interface(self):
        """Create the main chat interface."""
        # Use template manager CSS for professional styling
        css = self.template_manager.gradio_css

        with gr.Blocks(css=css) as chat_interface:
            # Header using Jinja2 template
            gr.HTML(self.template_manager.render_app_header())

            # Main interface - now more spacious without compliance analysis
            with gr.Row():
                with gr.Column(scale=3):
                    # Chat interface - wider now (using tuples for compatibility)
                    chatbot = gr.Chatbot(
                        value=[], 
                        height=600,
                        show_label=False,
                        container=True
                    )

                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Ask me anything about finance: 'Should I invest in index funds?' or 'How does compound interest work?'",
                            show_label=False,
                            scale=4,
                            container=False
                        )
                        submit_btn = gr.Button("Ask", variant="primary", scale=1)

                with gr.Column(scale=1):
                    # Prompt Version Selector
                    gr.HTML("<h4>🎯 AI Response Mode</h4>")
                    prompt_selector = gr.Dropdown(
                        choices=["Simple", "Compliant", "Strict", "Educational"],
                        value="Compliant",
                        label="Select Response Style",
                        info="Choose how the AI should respond to your questions"
                    )
                    
                    # Current prompt info
                    prompt_info = gr.Markdown(
                        value=self.get_current_prompt_info(),
                        show_label=False,
                        elem_classes=["validation-box"]
                    )
                    
                    # Validation status panel
                    gr.HTML("<h4>🛡️ Guardrails Status</h4>")
                    validation_status = gr.Markdown(
                        value="Ready to validate your financial questions and responses...",
                        show_label=False,
                        elem_classes=["validation-box"]
                    )

                    # API Status
                    gr.HTML("<h4>⚙️ System Status</h4>")
                    api_status = gr.HTML(self._get_api_status_html())

            # Examples section
            with gr.Row():
                gr.Examples(
                    examples=[
                        "What are the benefits of investing in index funds for retirement?",
                        "How does compound interest work with savings accounts?",
                        "Should I prioritize paying off debt or investing first?",
                        "What's the difference between stocks and bonds?",
                        "How much should I save for an emergency fund?",
                        "Is real estate a good investment for beginners?"
                    ],
                    inputs=msg_input,
                    label="💡 Example Questions"
                )

            # Event handlers
            def submit_question(question, history):
                updated_history, empty_input, validation_info = self.process_question(question, history)
                return updated_history, empty_input, validation_info
            
            def change_prompt_version(version):
                status_msg = self.set_prompt_version(version)
                updated_info = self.get_current_prompt_info()
                return updated_info, status_msg

            # Submit button and enter key
            submit_btn.click(
                fn=submit_question,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input, validation_status]
            )

            msg_input.submit(
                fn=submit_question,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input, validation_status]
            )
            
            # Prompt version change
            prompt_selector.change(
                fn=change_prompt_version,
                inputs=[prompt_selector],
                outputs=[prompt_info, validation_status]
            )

        return chat_interface
    
    def create_compliance_analysis_interface(self):
        """Create the dedicated compliance analysis interface."""
        with gr.Blocks() as analysis_interface:
            # Header using Jinja2 template
            compliance_header = self.template_manager.render_app_header(
                app_title="📊 Compliance Analysis Dashboard",
                app_subtitle="Detailed Before/After Comparison with Color-Coded Highlighting",
                app_description="See exactly how AI responses are enhanced for regulatory compliance"
            )
            gr.HTML(compliance_header)
            
            # Refresh button
            with gr.Row():
                refresh_btn = gr.Button("🔄 Refresh Analysis", variant="secondary", size="sm")
                analysis_status = gr.Markdown("**Status**: Waiting for analysis data...")
            
            # Main analysis display - full width for better viewing
            analysis_display = gr.HTML(
                value="<div style='padding: 40px; text-align: center; color: #6c757d; font-size: 18px;'>💬 Ask a question in the Chat tab first, then return here to see the detailed compliance analysis.</div>",
                show_label=False
            )
            
            # Analysis metadata
            with gr.Row():
                with gr.Column():
                    gr.HTML("<h4>📋 Analysis Details</h4>")
                    analysis_meta = gr.Markdown(
                        value="**Current Mode**: Compliant\n**Latest Analysis**: None available",
                        elem_classes=["validation-box"]
                    )
                
                with gr.Column():
                    gr.HTML(self.template_manager.render_usage_instructions())
            
            # Educational section using Jinja2 template
            with gr.Row():
                gr.HTML(self.template_manager.render_compliance_guide())
            
            # Event handlers
            def refresh_analysis():
                if self.latest_compliance_analysis:
                    status = f"**Status**: Analysis updated • **Mode**: {self.current_prompt_version.value.title()} • **Size**: {len(self.latest_compliance_analysis)} chars"
                    meta = f"**Current Mode**: {self.current_prompt_version.value.title()}\n**Latest Analysis**: Available\n**HTML Size**: {len(self.latest_compliance_analysis):,} characters"
                    return self.latest_compliance_analysis, status, meta
                else:
                    status = "**Status**: No analysis available - ask a question in the Chat tab first"
                    meta = f"**Current Mode**: {self.current_prompt_version.value.title()}\n**Latest Analysis**: None available"
                    return "<div style='padding: 40px; text-align: center; color: #6c757d; font-size: 18px;'>💬 No compliance analysis available yet. Ask a question in the Chat tab first!</div>", status, meta
            
            refresh_btn.click(
                fn=refresh_analysis,
                outputs=[analysis_display, analysis_status, analysis_meta]
            )
            
            # Auto-refresh on load
            analysis_interface.load(
                fn=refresh_analysis,
                outputs=[analysis_display, analysis_status, analysis_meta]
            )

        return analysis_interface
    
    def create_interface(self):
        """Create the complete multi-page interface."""
        # Create individual interfaces
        chat_interface = self.create_chat_interface()
        analysis_interface = self.create_compliance_analysis_interface()
        
        # Create tabbed interface
        demo = gr.TabbedInterface(
            [chat_interface, analysis_interface],
            ["💬 Chat", "📊 Compliance Analysis"],
            title="🏦 AI Financial Advisor with Guardrails",
            theme=gr.themes.Soft()
        )
        
        return demo

    def _get_api_status_html(self) -> str:
        """Generate HTML showing API and system status."""
        gemini_status = "✅ Connected" if self.model else "❌ Not configured (set GEMINI_API_KEY)"
        current_mode = self.current_prompt_version.value.title()
        
        services = {
            "Gemini API": gemini_status,
            "Current Mode": current_mode,
            "Prompt Guardrails": "✅ Active",
            "Response Guardrails": "✅ Active", 
            "Compliance Checks": "✅ SEC/FINRA Rules"
        }
        
        return self.template_manager.render_api_status(services)

    def launch(self, **kwargs):
        """Launch the Gradio interface."""
        demo = self.create_interface()

        # Default launch parameters
        default_kwargs = {
            "server_name": "0.0.0.0",
            "server_port": 7863,  # Different port to avoid conflicts
            "share": False,
            "debug": False,
            "show_api": False
        }

        # Update with user provided kwargs
        default_kwargs.update(kwargs)

        print("🚀 Launching Gradio Financial Advisor...")
        print(f"📍 Access at: http://localhost:{default_kwargs['server_port']}")
        print("🛡️ All responses validated for financial compliance")

        if not self.model:
            print("⚠️ WARNING: Gemini API not configured. Set GEMINI_API_KEY environment variable.")

        demo.launch(**default_kwargs)


def main():
    """Main entry point for the Gradio Financial Advisor."""
    print("🏦 AI Financial Advisor with Guardrails")
    print("=" * 50)
    
    # Initialize the advisor
    advisor = GradioFinancialAdvisor()
    
    # Launch with default settings
    advisor.launch(
        share=False,  # Set to True to create a public link
        debug=False,
        show_api=False,
        server_port=7860
    )


if __name__ == "__main__":
    main()
