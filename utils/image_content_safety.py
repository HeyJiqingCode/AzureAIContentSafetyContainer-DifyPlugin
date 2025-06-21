import requests
import base64
from typing import Optional, List, Dict, Any

def analyze_image_content_safety(
    api_endpoint: str,
    api_version: str,
    images: List[Dict[str, Any]],
    header_key: Optional[str] = None,
    header_value: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Analyze image content safety using Azure AI Content Safety API
    
    Args:
        api_endpoint: Azure API endpoint
        api_version: API version
        images: List of image file objects from Dify, containing remote_url
        header_key: Optional header key for authentication
        header_value: Optional header value for authentication
    
    Returns:
        List of API responses for each image
    """
    results = []
    headers = {
        "Content-Type": "application/json"
    }
    
    if header_key and header_value:
        headers[header_key] = header_value
    
    for image in images:
        api_url = f"{api_endpoint}/contentsafety/image:analyze?api-version={api_version}"
        remote_url = ""
        try:
            # Get remote_url from image file object
            remote_url = image.url
            if not remote_url:
                results.append({
                    "error": "Missing url in image file object",
                    "image": image
                })
                continue
                
            # Download image
            response = requests.get(remote_url, timeout=10)
            response.raise_for_status()
            
            # Convert to base64
            image_data = base64.b64encode(response.content).decode('utf-8')
            
            # Prepare API request
            payload = {
                "image": {
                    "content": image_data
                },
                "outputType": "FourSeverityLevels"
            }
            
            # Call API
            api_response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            api_response.raise_for_status()
            
            results.append(api_response.json())
            
        except requests.RequestException as e:
            results.append({
                "error": str(e),
                "image_url": remote_url
            })
    
    return results