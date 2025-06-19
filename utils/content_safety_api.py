import requests
from typing import Dict, Any, Optional, Union


def analyze_content_safety(
    api_endpoint: str,
    api_version: str,
    text: str,
    header_key: Optional[str] = None,
    header_value: Optional[str] = None,
    blocklist_names: Optional[list] = None,
    halt_on_blocklist_hit: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Call Azure AI Content Safety API to analyze text content
    
    Args:
        api_endpoint: Base API endpoint URL (e.g., https://your-endpoint.com)
        api_version: API version (e.g., 2024-09-01)
        text: Text content to analyze
        header_key: Optional custom header key
        header_value: Optional custom header value
        blocklist_names: Optional blocklist names list
        halt_on_blocklist_hit: Optional flag to halt when blocklist is hit
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        Exception: If API call fails
    """
    # Construct complete URL
    base_url = api_endpoint.rstrip('/')
    url = f"{base_url}/contentsafety/text:analyze?api-version={api_version}"
    
    # Set request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add optional custom header
    if header_key and header_value:
        headers[header_key] = header_value
    
    # Build request body
    data: Dict[str, Union[str, list, bool]] = {"text": text}
    
    # Add optional parameters
    if blocklist_names:
        data["blocklistNames"] = blocklist_names
    if halt_on_blocklist_hit is not None:
        data["haltOnBlocklistHit"] = halt_on_blocklist_hit
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Content Safety API call failed: {str(e)}")


def parse_content_safety_result(api_response: Dict[str, Any]) -> Dict[str, str]:
    """
    Parse Content Safety API response results
    
    Args:
        api_response: JSON response returned by API
        
    Returns:
        Parsed result dictionary containing CheckResult and possible Details
    """
    try:
        categories_analysis = api_response.get("categoriesAnalysis", [])
        
        # Check if any category has severity not equal to 0
        dangerous_categories = []
        for category in categories_analysis:
            category_name = category.get("category", "")
            severity = category.get("severity", 0)
            
            if severity > 0:
                dangerous_categories.append({
                    "category": category_name,
                    "severity": severity
                })
        
        if dangerous_categories:
            # Has dangerous content, return DENY
            # Build details_text (brief information in parentheses)
            details_parts = []
            for cat in dangerous_categories:
                details_parts.append(f"Category: {cat['category']}, SeverityLevel: {cat['severity']}")
            details_text = " ".join(details_parts)
            
            # Build detailed violation information
            violation_lines = []
            for i, cat in enumerate(dangerous_categories):
                if len(dangerous_categories) > 1:
                    # Multiple results end each line with semicolon
                    violation_lines.append(f"\n- **{cat['category']}** (SeverityLevel: {cat['severity']});")
                else:
                    # Single result without semicolon
                    violation_lines.append(f"\n- **{cat['category']}** (SeverityLevel: {cat['severity']})")
            
            # Assemble final Details format
            violation_text = "\n".join(violation_lines)
            details = f"## Harmful Content Detected !\n Your input contains harmful information(e.g., **hate and fairness**, **sexual**, **violence**, or **self-harm**), please remove or modify such content and try again!\n___\n**Detected Categories:**{violation_text}\n> Severity levels range from 0 (lowest) to 7 (highest)"
            
            return {
                "CheckResult": "DENY",
                "Details": details
            }
        else:
            # No dangerous content, return ALLOW
            return {
                "CheckResult": "ALLOW"
            }
            
    except Exception as e:
        raise Exception(f"Failed to parse Content Safety results: {str(e)}")
