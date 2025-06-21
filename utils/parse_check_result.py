from typing import Dict, Any, List, Optional

def parse_check_result(
    text_response: Optional[Dict[str, Any]], 
    image_responses: Optional[List[Dict[str, Any]]]
) -> Dict[str, Any]:
    try:
        final_check_result = "ALLOW"
        all_blocklist_items = []
        all_dangerous_categories = []
        
        raw_results = {
            "text": text_response or {},
            "image": image_responses or []
        }

        # Process text response
        if text_response:
            # Handle blocklist matches
            blocklists_match = text_response.get("blocklistsMatch", [])
            for item in blocklists_match:
                all_blocklist_items.append(item.get("blocklistItemText", ""))
            
            # Handle category analysis
            text_categories = text_response.get("categoriesAnalysis", [])
            for category in text_categories:
                if category.get("severity", 0) > 0:
                    all_dangerous_categories.append({
                        "source": "text",
                        "category": category.get("category"),
                        "severity": category.get("severity")
                    })

        # Process image responses
        if image_responses:
            for image_response in image_responses:
                # Handle errors from image analysis function
                if "error" in image_response:
                    all_dangerous_categories.append({
                        "source": "image",
                        "category": f"Processing Error: {image_response['error']}",
                        "severity": "N/A"
                    })
                    continue
                
                image_categories = image_response.get("categoriesAnalysis", [])
                for category in image_categories:
                    if category.get("severity", 0) > 0:
                        all_dangerous_categories.append({
                            "source": "image",
                            "category": category.get("category"),
                            "severity": category.get("severity")
                        })
        
        # Determine final result
        if all_blocklist_items or all_dangerous_categories:
            final_check_result = "DENY"

        # Build response
        if final_check_result == "DENY":
            details = "## Harmful Content Detected !\n\n"
            details += "Your input contains harmful information(e.g., **hate and fairness**, **sexual**, **violence**, or **self-harm**), please remove or modify such content and try again!\n\n"
            details += "___\n\n"

            if all_blocklist_items:
                details += "### BlockListsMatched:\n\n"
                details += ", ".join([f"`{item}`" for item in all_blocklist_items])
                details += "\n\n"

            if all_dangerous_categories:
                details += "### CategoriesAnalysis:\n\n"
                num_categories = len(all_dangerous_categories)
                for cat in all_dangerous_categories:
                    # Format the line with inline code for source and bold for category
                    line = f"- `{cat['source']}` **{cat['category']}** (SeverityLevel: {cat['severity']})"
                    # Add a semicolon only if there are multiple categories
                    if num_categories > 1:
                        line += ";"
                    details += f"{line}\n"
                details += "\n> Text severity: 0–7; Image severity: 0, 2, 4, 6; higher means more severe.\n"
            
            return {"CheckResult": "DENY", "Details": details, "RawResults": raw_results}
        else:
            return {"CheckResult": "ALLOW", "Details": "", "RawResults": raw_results}
            
    except Exception as e:
        raise Exception(f"Failed to parse Content Safety results: {str(e)}")
