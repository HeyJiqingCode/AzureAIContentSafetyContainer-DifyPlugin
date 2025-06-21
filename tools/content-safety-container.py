from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Import utility functions
from utils.text_content_safety import analyze_text_content_safety
from utils.image_content_safety import analyze_image_content_safety
from utils.parse_check_result import parse_check_result

class ContentSafetyContainerTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Analyze text and image content safety using Azure AI Content Safety API"""
        
        # Get text and image to analyze from tool parameters
        text = tool_parameters.get("text", "")
        images = tool_parameters.get("image", [])
        
        # If no content, return a message
        if not text and not images:
            yield self.create_text_message("No text or image provided for analysis.")
            return

        # Get configuration information from credentials
        credentials = self.runtime.credentials
        api_endpoint = credentials.get("api_endpoint", "")
        api_version = credentials.get("api_version", "")
        header_key = credentials.get("header_key")
        header_value = credentials.get("header_value")

        text_api_response = None
        image_api_response = None

        try:
            # Analyze text if provided
            if text:
                halt_on_blocklist_hit_param = tool_parameters.get("halt_on_blocklist_hit")
                if isinstance(halt_on_blocklist_hit_param, str):
                    halt_on_blocklist_hit = halt_on_blocklist_hit_param.lower() == 'true'
                else:
                    halt_on_blocklist_hit = bool(halt_on_blocklist_hit_param) if halt_on_blocklist_hit_param is not None else None
                
                blocklist_names_str = tool_parameters.get("blocklist_names")
                blocklist_names = [name.strip() for name in blocklist_names_str.split(',')] if blocklist_names_str else None

                text_api_response = analyze_text_content_safety(
                    api_endpoint=api_endpoint, api_version=api_version, text=text,
                    header_key=header_key, header_value=header_value,
                    blocklist_names=blocklist_names, halt_on_blocklist_hit=halt_on_blocklist_hit
                )

            # Analyze images if provided
            if images:
                image_api_response = analyze_image_content_safety(
                    api_endpoint=api_endpoint, api_version=api_version, images=images,
                    header_key=header_key, header_value=header_value
                )
            
            # Parse combined API responses
            result = parse_check_result(text_api_response, image_api_response)
            
            # Return final results
            yield self.create_json_message(result)
            if result.get("CheckResult") == "DENY":
                yield self.create_text_message(result.get("Details", ""))
            else:
                yield self.create_text_message("Content safety check passed.")
            
            yield self.create_variable_message("CheckResult", result.get("CheckResult"))
            yield self.create_variable_message("Details", result.get("Details", ""))
            yield self.create_variable_message("RawResults", result.get("RawResults", {}))

        except Exception as e:
            error_msg = f"Content safety analysis failed: {str(e)}"
            yield self.create_text_message(error_msg)
            yield self.create_variable_message("CheckResult", "ERROR")
            yield self.create_variable_message("Details", error_msg)
