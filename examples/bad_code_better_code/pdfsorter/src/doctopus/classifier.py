from typing import Optional, Dict, Any

def classify_document(content: str, config: Dict[str, Any]) -> Optional[str]:
    """Classify document based on content triggers."""
    categories = config.get("categories", {})
    for category, rules in categories.items():
        triggers = rules.get("triggers", [])
        if all(trigger in content for trigger in triggers):
            return category
    return None