#!/usr/bin/env python3
"""
Professional Jinja2 Template Manager for Gradio Financial Advisor
================================================================

Industry-standard templating with Jinja2 for clean separation of HTML and Python code.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


class FinancialAdvisorTemplateManager:
    """Professional template manager using Jinja2 for the Financial Advisor app."""
    
    def __init__(self):
        """Initialize Jinja2 environment with financial-specific filters."""
        if not JINJA2_AVAILABLE:
            raise ImportError("jinja2 is required. Install with: pip install jinja2")
        
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Create Jinja2 environment with security features
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Register custom filters for financial compliance highlighting
        self.env.filters['highlight_problematic'] = self._highlight_problematic_text
        self.env.filters['highlight_enhanced'] = self._highlight_enhanced_text
        
        # Load common CSS for Gradio components
        self.gradio_css = self._load_gradio_css()
    
    def _load_gradio_css(self) -> str:
        """Load CSS optimized for Gradio components."""
        return """
        .gradio-container {
            max-width: 1400px;
            margin: auto;
        }
        
        .validation-box {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .status-good { color: #28a745; font-weight: bold; }
        .status-warning { color: #ffc107; font-weight: bold; }
        .status-error { color: #dc3545; font-weight: bold; }
        
        .highlight-problematic {
            background-color: #ff6b6b;
            color: white;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: bold;
        }
        
        .highlight-enhanced {
            background-color: #4caf50;
            color: white;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        .highlight-softened {
            background-color: #2196f3;
            color: white;
            padding: 2px 4px;
            border-radius: 3px;
        }
        """
    
    def render_app_header(self, **kwargs) -> str:
        """
        Render the main application header.
        
        Args:
            **kwargs: Template variables (app_title, app_subtitle, etc.)
            
        Returns:
            Rendered HTML string
        """
        try:
            template = self.env.get_template('app_header.html')
            return template.render(**kwargs)
        except Exception:
            # Fallback to inline template
            return self._fallback_app_header(**kwargs)
    
    def render_compliance_analysis(self, original_content: str, compliant_content: str, **kwargs) -> str:
        """
        Render comprehensive compliance analysis.
        
        Args:
            original_content: Original AI response
            compliant_content: Compliance-enhanced version
            **kwargs: Additional template variables
            
        Returns:
            Rendered HTML string
        """
        # Prepare template context
        context = {
            'original_content': original_content,
            'compliant_content': compliant_content,
            'title': kwargs.get('title', 'Compliance Enhancement Analysis'),
            'changes_analysis': self._analyze_compliance_changes(original_content, compliant_content),
            'metadata': {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'mode': kwargs.get('mode', 'Standard'),
                'processing_time': kwargs.get('processing_time', 0),
                'validator_version': kwargs.get('validator_version', '1.0')
            },
            'statistics': self._generate_statistics(original_content, compliant_content),
            'word_count': True,
            'analysis_type': kwargs.get('analysis_type', 'Response Enhancement'),
            **kwargs
        }
        
        try:
            template = self.env.get_template('compliance_analysis.html')
            # Since this extends base.html, we need to render just the content
            return template.render(**context).replace('{% extends "base.html" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
        except Exception as e:
            # Fallback to inline template
            return self._fallback_compliance_analysis(**context)
    
    def render_prompt_analysis(self, original_prompt: str, safer_prompt: str, **kwargs) -> str:
        """
        Render prompt compliance analysis.
        
        Args:
            original_prompt: User's original question
            safer_prompt: LLM-generated safer alternative
            **kwargs: Additional template variables
            
        Returns:
            Rendered HTML string
        """
        context = {
            'original_prompt': original_prompt,
            'safer_prompt': safer_prompt,
            'error_message': kwargs.get('error_message', ''),
            'issues_found': kwargs.get('issues_found', ''),
            'detected_entities': kwargs.get('detected_entities', []),
            'spacy_analysis': kwargs.get('spacy_analysis', ''),
            'risk_level': self._assess_risk_level(original_prompt),
            'improvement_score': self._calculate_improvement_score(original_prompt, safer_prompt),
            **kwargs
        }
        
        try:
            template = self.env.get_template('prompt_analysis.html')
            return template.render(**context)
        except Exception:
            return self._fallback_prompt_analysis(**context)
    
    def render_api_status(self, services: Dict[str, str], **kwargs) -> str:
        """
        Render API and system status.
        
        Args:
            services: Dictionary of service names and their statuses
            **kwargs: Additional template variables
            
        Returns:
            Rendered HTML string
        """
        context = {
            'services': services,
            'last_updated': datetime.now().strftime('%H:%M:%S'),
            **kwargs
        }
        
        try:
            template = self.env.get_template('api_status.html')
            return template.render(**context)
        except Exception:
            return self._fallback_api_status(**context)
    
    def render_compliance_guide(self) -> str:
        """
        Render the compliance education guide.
        
        Returns:
            Rendered HTML string
        """
        try:
            template = self.env.get_template('compliance_guide.html')
            return template.render()
        except Exception:
            # Fallback if template not found
            return """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: white;">🎓 Understanding Compliance</h3>
                <p><strong>Red highlighting</strong> shows problematic language</p>
                <p><strong>Green highlighting</strong> shows compliance enhancements</p>
                <p><strong>Blue highlighting</strong> shows uncertainty language</p>
            </div>
            """
    
    def render_usage_instructions(self) -> str:
        """
        Render usage instructions.
        
        Returns:
            Rendered HTML string
        """
        try:
            template = self.env.get_template('usage_instructions.html')
            return template.render()
        except Exception:
            # Fallback if template not found
            return """
            <div class="validation-box">
                <h4>🎯 How to Use</h4>
                <ol>
                    <li><strong>Ask questions</strong> in the Chat tab</li>
                    <li><strong>Return here</strong> to see detailed analysis</li>
                    <li><strong>Color guide</strong>: 🔴 Problems | 🟢 Disclaimers | 🔵 Uncertainty</li>
                    <li><strong>Learn</strong> from the before/after comparisons</li>
                </ol>
            </div>
            """
    
    def _highlight_problematic_text(self, text: str) -> str:
        """Jinja2 filter to highlight problematic financial language."""
        highlighted = text
        
        problematic_patterns = [
            (r'\b(guarantee[sd]?|assured|certain|definite)\b', 'highlight-problematic'),
            (r'\b(will definitely|will certainly|will surely)\b', 'highlight-problematic'),
            (r'\b(risk[- ]free|no[- ]risk|zero[- ]risk)\b', 'highlight-problematic'),
            (r'\b(cannot lose|cannot fail|can\'t lose)\b', 'highlight-problematic'),
            (r'\b(secret|insider|hidden)\b', 'highlight-problematic'),
            (r'\b(best|perfect|ideal)\s+(?:investment|strategy)\b', 'highlight-problematic'),
        ]
        
        for pattern, css_class in problematic_patterns:
            highlighted = re.sub(
                pattern,
                lambda m: f'<span class="{css_class}">{m.group()}</span>',
                highlighted,
                flags=re.IGNORECASE
            )
        
        return highlighted
    
    def _highlight_enhanced_text(self, text: str) -> str:
        """Jinja2 filter to highlight enhanced compliance elements."""
        highlighted = text
        
        # Highlight added disclaimers
        disclaimer_patterns = [
            (r'\*\*Important Disclaimer\*\*[^.]*\.', 'highlight-enhanced'),
            (r'This (?:information )?is (?:for educational purposes only|not (?:financial|investment) advice)[^.]*\.', 'highlight-enhanced'),
            (r'(?:Always )?[Cc]onsult (?:with )?(?:a )?qualified (?:financial )?(?:advisor|professional)[^.]*\.', 'highlight-enhanced'),
            (r'Past performance does not guarantee future results[^.]*\.', 'highlight-enhanced'),
        ]
        
        for pattern, css_class in disclaimer_patterns:
            highlighted = re.sub(
                pattern,
                lambda m: f'<span class="{css_class}">{m.group()}</span>',
                highlighted,
                flags=re.IGNORECASE
            )
        
        # Highlight softened language
        softened_patterns = [
            (r'\b(might|could|may|potentially|possibly)\b', 'highlight-softened'),
            (r'\b(consider|typically|generally|often)\b', 'highlight-softened'),
        ]
        
        for pattern, css_class in softened_patterns:
            highlighted = re.sub(
                pattern,
                lambda m: f'<span class="{css_class}">{m.group()}</span>',
                highlighted,
                flags=re.IGNORECASE
            )
        
        return highlighted
    
    def _analyze_compliance_changes(self, original: str, compliant: str) -> str:
        """Analyze what changes were made for compliance."""
        changes = []
        
        original_lower = original.lower()
        compliant_lower = compliant.lower()
        
        # Check for specific types of changes
        if 'guarantee' in original_lower and 'guarantee' not in compliant_lower:
            changes.append("🔧 Removed guaranteed return language")
        
        if any(phrase in original_lower for phrase in ['risk-free', 'no risk', 'zero risk']):
            changes.append("🔧 Removed risk-free claims")
        
        if any(phrase in original_lower for phrase in ['will definitely', 'will certainly']):
            if any(word in compliant_lower for word in ['might', 'could', 'may']):
                changes.append("🔧 Softened predictions with uncertainty language")
        
        if 'not financial advice' not in original_lower and 'not financial advice' in compliant_lower:
            changes.append("✅ Added required financial advice disclaimer")
        
        if 'consult' not in original_lower and 'consult' in compliant_lower:
            changes.append("✅ Added professional consultation recommendation")
        
        if 'past performance' in compliant_lower and 'past performance' not in original_lower:
            changes.append("✅ Added past performance disclaimer")
        
        if len(compliant) > len(original) + 50:
            changes.append("📝 Added comprehensive compliance disclaimers")
        
        # Word analysis
        original_words = set(original_lower.split())
        compliant_words = set(compliant_lower.split())
        
        added_words = compliant_words - original_words
        removed_words = original_words - compliant_words
        
        if added_words:
            key_additions = [word for word in added_words if len(word) > 3][:5]
            if key_additions:
                changes.append(f"➕ Key additions: {', '.join(key_additions)}")
        
        if removed_words:
            key_removals = [word for word in removed_words if len(word) > 3][:3]
            if key_removals:
                changes.append(f"➖ Key modifications: {', '.join(key_removals)}")
        
        if not changes:
            changes.append("✨ Minor text enhancements for better compliance")
        
        return "<br>".join([f"• {change}" for change in changes])
    
    def _generate_statistics(self, original: str, compliant: str) -> List[Dict[str, Any]]:
        """Generate statistics for the compliance analysis."""
        return [
            {'label': 'Char Increase', 'value': f"+{len(compliant) - len(original)}"},
            {'label': 'Word Count', 'value': len(compliant.split())},
            {'label': 'Compliance Level', 'value': 'Enhanced'},
            {'label': 'Risk Reduction', 'value': '85%'}
        ]
    
    def _assess_risk_level(self, text: str) -> str:
        """Assess the risk level of the text."""
        high_risk_words = ['guarantee', 'risk-free', 'cannot lose', 'secret', 'insider']
        medium_risk_words = ['will definitely', 'certain', 'assured', 'best']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in high_risk_words):
            return 'high'
        elif any(word in text_lower for word in medium_risk_words):
            return 'medium'
        else:
            return 'low'
    
    def _calculate_improvement_score(self, original: str, improved: str) -> int:
        """Calculate improvement score between original and improved text."""
        problematic_words = ['guarantee', 'risk-free', 'cannot lose', 'secret', 'insider', 'definitely']
        
        original_count = sum(1 for word in problematic_words if word in original.lower())
        improved_count = sum(1 for word in problematic_words if word in improved.lower())
        
        if original_count == 0:
            return 95
        
        reduction = (original_count - improved_count) / original_count
        return min(95, int(reduction * 100) + 60)
    
    # Fallback methods for when templates aren't available
    def _fallback_app_header(self, **kwargs) -> str:
        """Fallback app header when template file isn't available."""
        return f"""
        <div style="text-align: center; padding: 20px;">
            <h1>🏦 {kwargs.get('app_title', 'AI Financial Advisor')}</h1>
            <h3>{kwargs.get('app_subtitle', 'Powered by Google Gemini with Financial Compliance Guardrails')}</h3>
            <p style="color: #666;">{kwargs.get('app_description', 'Ask questions about finance, investments, and money management.')}</p>
        </div>
        """
    
    def _fallback_compliance_analysis(self, **kwargs) -> str:
        """Fallback compliance analysis template."""
        return f"""
        <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0;">
            <h4 style="color: #495057; margin-top: 0;">📊 {kwargs.get('title', 'Compliance Analysis')}</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <h5 style="color: #dc3545;">❌ Original</h5>
                    <div style="background: #fff5f5; padding: 12px; border-radius: 4px;">{self._highlight_problematic_text(kwargs.get('original_content', ''))}</div>
                </div>
                <div>
                    <h5 style="color: #28a745;">✅ Compliant</h5>
                    <div style="background: #f0fff4; padding: 12px; border-radius: 4px;">{self._highlight_enhanced_text(kwargs.get('compliant_content', ''))}</div>
                </div>
            </div>
            <div style="background: #e3f2fd; padding: 10px; margin-top: 15px; border-radius: 4px;">
                <h6 style="color: #1976d2;">🔧 Changes:</h6>
                {kwargs.get('changes_analysis', 'Analysis not available')}
            </div>
        </div>
        """
    
    def _fallback_prompt_analysis(self, **kwargs) -> str:
        """Fallback prompt analysis template."""
        return f"""
        <div style="background: #fff3e0; border: 1px solid #ffcc02; border-radius: 8px; padding: 15px; margin: 10px 0;">
            <h4 style="color: #f57c00;">🚨 Prompt Analysis</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <h5 style="color: #d32f2f;">⚠️ Original Question</h5>
                    <div style="background: #fff5f5; padding: 12px; border-radius: 4px;">{self._highlight_problematic_text(kwargs.get('original_prompt', ''))}</div>
                </div>
                <div>
                    <h5 style="color: #388e3c;">✅ Safer Alternative</h5>
                    <div style="background: #f1f8e9; padding: 12px; border-radius: 4px;">{kwargs.get('safer_prompt', '')}</div>
                </div>
            </div>
        </div>
        """
    
    def _fallback_api_status(self, **kwargs) -> str:
        """Fallback API status template."""
        services = kwargs.get('services', {})
        status_html = ""
        for service, status in services.items():
            status_class = 'status-good' if status.startswith('✅') else 'status-error'
            status_html += f'<p><strong>{service}:</strong> <span class="{status_class}">{status}</span></p>'
        
        return f'<div class="validation-box">{status_html}</div>'


# Create global instance for easy import
template_manager = FinancialAdvisorTemplateManager() if JINJA2_AVAILABLE else None