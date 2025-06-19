from typing import Any
import requests

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

# Import utility functions for actual API validation
from utils.content_safety_api import analyze_content_safety


class ContentSafetyContainerProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate credential configuration for Azure AI Content Safety Container
        """
        try:
            # Get required credentials
            api_endpoint = credentials.get("api_endpoint")
            api_version = credentials.get("api_version")
            
            if not api_endpoint:
                raise ToolProviderCredentialValidationError("API endpoint is required")
            
            if not api_version:
                raise ToolProviderCredentialValidationError("API version is required")
            
            # Validate endpoint format
            if not api_endpoint.startswith(("http://", "https://")):
                raise ToolProviderCredentialValidationError("API endpoint must start with http:// or https://")
            
            # Get optional authentication information
            header_key = credentials.get("header_key")
            header_value = credentials.get("header_value")
            
            # Perform actual API validation by making a test call
            try:
                # Use simple "test" as test content for validation
                validation_text = "test"
                
                # Call the API using the updated utility function
                api_response = analyze_content_safety(
                    api_endpoint=api_endpoint,
                    api_version=api_version,
                    text=validation_text,
                    header_key=header_key,
                    header_value=header_value
                )
                
                # If we got here, the API call succeeded
                print(f"✅ Configuration validation passed:")
                print(f"  Base endpoint: {api_endpoint}")
                print(f"  API version: {api_version}")
                print(f"  Full URL: {api_endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={api_version}")
                print(f"  API connectivity: Successfully connected")
                
                # Only display when Header is actually configured
                if header_key and header_value:
                    print(f"  Authentication header: {header_key}: [Configured and verified]")
                else:
                    print("  Authentication header: Not configured (optional)")
                
                return
                
            except Exception as api_error:
                # API call failed, provide specific error information
                error_msg = str(api_error)
                if "timeout" in error_msg.lower():
                    raise ToolProviderCredentialValidationError("API endpoint connection timeout, please check if the service is running and accessible")
                elif "connection" in error_msg.lower():
                    raise ToolProviderCredentialValidationError("Unable to connect to API endpoint, please check if the endpoint URL is correct")
                elif "401" in error_msg or "403" in error_msg or "unauthorized" in error_msg.lower():
                    raise ToolProviderCredentialValidationError("API authentication failed, please check if the header key and value are correct")
                elif "404" in error_msg:
                    raise ToolProviderCredentialValidationError("API endpoint not found, please check if the endpoint path is correct")
                else:
                    raise ToolProviderCredentialValidationError(f"API validation failed: {error_msg}")
                
        except ToolProviderCredentialValidationError:
            # Re-raise our validation errors
            raise
        except Exception as e:
            # For other unexpected errors, provide generic hint
            print(f"Error occurred during validation: {str(e)}")
            raise ToolProviderCredentialValidationError(f"Configuration validation failed: {str(e)}")
