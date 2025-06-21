import requests
from typing import Dict, Any, Optional, Union

def analyze_text_content_safety(
    api_endpoint: str,
    api_version: str,
    text: str,
    header_key: Optional[str] = None,
    header_value: Optional[str] = None,
    blocklist_names: Optional[list] = None,
    halt_on_blocklist_hit: Optional[bool] = None
) -> Dict[str, Any]:

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
