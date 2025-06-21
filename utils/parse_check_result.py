from typing import Dict, Any

def parse_check_result(api_response: Dict[str, Any]) -> Dict[str, str]:
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
                    violation_lines.append(f"\n- `text` **{cat['category']}** (SeverityLevel: {cat['severity']});")
                else:
                    # Single result without semicolon
                    violation_lines.append(f"\n- `text` **{cat['category']}** (SeverityLevel: {cat['severity']})")
            
            # Assemble final Details format
            violation_text = "\n".join(violation_lines)
            details = f"## Harmful Content Detected !\n Your input contains harmful information(e.g., **hate and fairness**, **sexual**, **violence**, or **self-harm**), please remove or modify such content and try again!\n___\n**Details:**{violation_text}\n> Text severity: 0–7; Image severity: 0, 2, 4, 6; higher means more severe."
            
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
