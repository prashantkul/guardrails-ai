import re
import socket
import requests
from urllib.parse import urlparse
from typing import Dict, Any, List
import validators
from guardrails.errors import ValidationError


def url_validator(value: str, allowed_schemes: List[str] = None, 
                 blocked_domains: List[str] = None, check_reachability: bool = False) -> str:
    """Validator function for URL validation"""
    value = value.strip()
    allowed_schemes = allowed_schemes or ['http', 'https']
    blocked_domains = blocked_domains or []
    
    # Basic URL validation
    if not validators.url(value):
        raise ValidationError(f"Invalid URL format: {value}")
    
    # Parse URL
    parsed = urlparse(value)
    
    # Check scheme
    if parsed.scheme not in allowed_schemes:
        raise ValidationError(
            f"URL scheme '{parsed.scheme}' not allowed. "
            f"Allowed schemes: {allowed_schemes}"
        )
    
    # Check blocked domains
    domain = parsed.netloc.lower()
    for blocked in blocked_domains:
        if blocked.lower() in domain:
            raise ValidationError(f"Domain '{domain}' is blocked")
    
    # Check reachability
    if check_reachability:
        try:
            response = requests.head(value, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                raise ValidationError(f"URL not reachable (status: {response.status_code})")
        except requests.RequestException as e:
            raise ValidationError(f"URL not reachable: {str(e)}")
    
    return value


def ip_address_validator(value: str, allow_private: bool = False, 
                        allow_localhost: bool = True, version: int = None) -> str:
    """Validator function for IP address validation"""
    value = value.strip()
    
    # Validate IP format
    is_valid_ipv4 = validators.ipv4(value)
    is_valid_ipv6 = validators.ipv6(value)
    
    if not (is_valid_ipv4 or is_valid_ipv6):
        raise ValidationError(f"Invalid IP address format: {value}")
    
    # Check version restriction
    if version == 4 and not is_valid_ipv4:
        raise ValidationError(f"Only IPv4 addresses allowed: {value}")
    elif version == 6 and not is_valid_ipv6:
        raise ValidationError(f"Only IPv6 addresses allowed: {value}")
    
    # Check private IP
    if not allow_private and _is_private_ip(value):
        raise ValidationError(f"Private IP addresses not allowed: {value}")
    
    # Check localhost
    if not allow_localhost and _is_localhost(value):
        raise ValidationError(f"Localhost addresses not allowed: {value}")
    
    return value


def domain_validator(value: str, check_dns: bool = False, 
                    allowed_tlds: List[str] = None, min_length: int = 3) -> str:
    """Validator function for domain validation"""
    value = value.strip().lower()
    
    # Basic domain validation
    if not validators.domain(value):
        raise ValidationError(f"Invalid domain format: {value}")
    
    # Check minimum length
    if len(value) < min_length:
        raise ValidationError(f"Domain too short (min {min_length} chars): {value}")
    
    # Check TLD restriction
    if allowed_tlds:
        domain_tld = value.split('.')[-1]
        if domain_tld not in allowed_tlds:
            raise ValidationError(
                f"TLD '{domain_tld}' not allowed. "
                f"Allowed TLDs: {allowed_tlds}"
            )
    
    # DNS lookup
    if check_dns:
        try:
            socket.gethostbyname(value)
        except socket.gaierror:
            raise ValidationError(f"Domain does not resolve: {value}")
    
    return value


def email_domain_validator(value: str, allowed_domains: List[str] = None, 
                          blocked_domains: List[str] = None, check_mx: bool = False) -> str:
    """Validator function for email domain validation"""
    value = value.strip().lower()
    allowed_domains = allowed_domains or []
    blocked_domains = blocked_domains or []
    
    # Basic email validation
    if not validators.email(value):
        raise ValidationError(f"Invalid email format: {value}")
    
    # Extract domain
    domain = value.split('@')[1]
    
    # Check allowed domains
    if allowed_domains and domain not in allowed_domains:
        raise ValidationError(
            f"Email domain '{domain}' not allowed. "
            f"Allowed domains: {allowed_domains}"
        )
    
    # Check blocked domains
    if domain in blocked_domains:
        raise ValidationError(f"Email domain '{domain}' is blocked")
    
    # Check MX record (simplified)
    if check_mx:
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                raise ValidationError(f"No MX record found for domain: {domain}")
        except ImportError:
            # dnspython not available, skip MX check
            pass
        except Exception as e:
            raise ValidationError(f"MX record check failed for {domain}: {str(e)}")
    
    return value


def _is_private_ip(ip: str) -> bool:
    """Check if IP is in private range"""
    import ipaddress
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except:
        return False


def _is_localhost(ip: str) -> bool:
    """Check if IP is localhost"""
    localhost_patterns = ['127.', '::1', 'localhost']
    return any(pattern in ip.lower() for pattern in localhost_patterns)


class InfrastructureGuard:
    """Simple guardrail for infrastructure validation"""
    
    def __init__(self, validator_type: str, **kwargs):
        self.validator_type = validator_type
        self.kwargs = kwargs
        
        # Validate validator type
        valid_types = ['url', 'ip', 'domain', 'email_domain']
        if validator_type not in valid_types:
            raise ValueError(f"Unknown validator type: {validator_type}")
    
    def validate(self, value: str) -> str:
        """Validate the input text"""
        if self.validator_type == 'url':
            return url_validator(value, **self.kwargs)
        elif self.validator_type == 'ip':
            return ip_address_validator(value, **self.kwargs)
        elif self.validator_type == 'domain':
            return domain_validator(value, **self.kwargs)
        elif self.validator_type == 'email_domain':
            return email_domain_validator(value, **self.kwargs)
        else:
            raise ValueError(f"Unknown validator type: {self.validator_type}")


def create_infrastructure_guard(validator_type: str, **kwargs) -> InfrastructureGuard:
    """Create an infrastructure validation guardrail"""
    return InfrastructureGuard(validator_type, **kwargs)


def demo_infrastructure_validation():
    """Demo function to test infrastructure validation"""
    results = {}
    
    # Test URL validation
    guard_url = create_infrastructure_guard(
        'url', 
        blocked_domains=['malicious.com', 'spam.net'],
        check_reachability=False  # Set to True to actually check URLs
    )
    
    test_urls = [
        "https://www.google.com",
        "http://example.com/path?query=1",
        "ftp://files.example.com",
        "https://malicious.com/page",
        "not-a-url"
    ]
    
    results['url'] = []
    for url in test_urls:
        try:
            validated = guard_url.validate(url)
            results['url'].append({"input": url, "status": "PASSED", "output": validated})
        except Exception as e:
            results['url'].append({"input": url, "status": "FAILED", "reason": str(e)})
    
    # Test IP validation
    guard_ip = create_infrastructure_guard(
        'ip', 
        allow_private=False,
        allow_localhost=True,
        version=4
    )
    
    test_ips = [
        "8.8.8.8",
        "192.168.1.1",
        "127.0.0.1",
        "::1",
        "not-an-ip"
    ]
    
    results['ip'] = []
    for ip in test_ips:
        try:
            validated = guard_ip.validate(ip)
            results['ip'].append({"input": ip, "status": "PASSED", "output": validated})
        except Exception as e:
            results['ip'].append({"input": ip, "status": "FAILED", "reason": str(e)})
    
    # Test domain validation
    guard_domain = create_infrastructure_guard(
        'domain',
        allowed_tlds=['com', 'org', 'net'],
        check_dns=False  # Set to True to actually check DNS
    )
    
    test_domains = [
        "google.com",
        "example.org",
        "test.xyz",
        "localhost",
        "invalid..domain"
    ]
    
    results['domain'] = []
    for domain in test_domains:
        try:
            validated = guard_domain.validate(domain)
            results['domain'].append({"input": domain, "status": "PASSED", "output": validated})
        except Exception as e:
            results['domain'].append({"input": domain, "status": "FAILED", "reason": str(e)})
    
    # Test email domain validation
    guard_email = create_infrastructure_guard(
        'email_domain',
        blocked_domains=['tempmail.com', 'guerrillamail.com']
    )
    
    test_emails = [
        "user@gmail.com",
        "test@company.org",
        "spam@tempmail.com",
        "invalid-email",
        "user@nonexistent-domain-12345.com"
    ]
    
    results['email_domain'] = []
    for email in test_emails:
        try:
            validated = guard_email.validate(email)
            results['email_domain'].append({"input": email, "status": "PASSED", "output": validated})
        except Exception as e:
            results['email_domain'].append({"input": email, "status": "FAILED", "reason": str(e)})
    
    return results