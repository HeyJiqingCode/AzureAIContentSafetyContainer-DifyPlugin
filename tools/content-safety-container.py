from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Import utility functions
from utils.text_content_safety import analyze_text_content_safety
from utils.parse_check_result import parse_check_result

class ContentSafetyContainerTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Analyze text content safety using Azure AI Content Safety API"""
        
        # Get text to analyze from tool parameters
        text = tool_parameters.get("text", "")
        
        # Parameter validation
        if not text:
            yield self.create_text_message("Error: Text content to analyze is a required parameter")
            return
        
        # Get configuration information from credentials
        credentials = self.runtime.credentials
        api_endpoint = credentials.get("api_endpoint", "")
        api_version = credentials.get("api_version", "")
        
        # Get optional Header information
        header_key = credentials.get("header_key")
        header_value = credentials.get("header_value")
        
        # Get optional parameters
        halt_on_blocklist_hit = tool_parameters.get("halt_on_blocklist_hit")
        
        # Process blocklist_names parameter
        blocklist_names = None
        blocklist_names_str = tool_parameters.get("blocklist_names")
        if blocklist_names_str:
            # Convert comma-separated string to list
            blocklist_names = [name.strip() for name in blocklist_names_str.split(",") if name.strip()]
        
        try:
            # Call Content Safety API
            api_response = analyze_text_content_safety(
                api_endpoint=api_endpoint,
                api_version=api_version,
                text=text,
                header_key=header_key,
                header_value=header_value,
                blocklist_names=blocklist_names,
                halt_on_blocklist_hit=halt_on_blocklist_hit
            )
            
            # Parse API response
            result = parse_check_result(api_response)
            
            # Return parsed results
            yield self.create_json_message(result)
            
            # Return different text messages based on check results
            if result["CheckResult"] == "DENY":
                yield self.create_text_message(result["Details"])
                yield self.create_variable_message("CheckResult", "DENY")
                yield self.create_variable_message("Details", result["Details"])
            else:
                yield self.create_text_message("Content safety check passed")
                yield self.create_variable_message("CheckResult", "ALLOW")
                
        except Exception as e:
            # Error handling
            error_msg = f"Content safety analysis failed: {str(e)}"
            yield self.create_text_message(error_msg)
            yield self.create_variable_message("CheckResult", "ERROR")
            yield self.create_variable_message("Details", error_msg)
