import re
from typing import List, Optional, Any
from dateutil import parser

class _MetadataExtractor:
    """Extracts metadata like dates and invoice IDs."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def extract_date(self, lines: List[str]) -> Optional[str]:
        """Extract first valid date from lines."""
        date_patterns = self.config.get("metadata_triggers", {}).get("date_patterns", [])
        if not date_patterns:
            date_patterns = [r'\b(?:\d{1,2}(?:st|nd|rd|th)?[ ./-](?:\d{1,2}|[a-zA-Z]+)[ ./-]\d{2,4})\b']

        date_list = []
        for line in lines:
            for pattern in date_patterns:
                match = re.search(pattern, line)
                if match:
                    date_list.append(match.group())

        for date_str in date_list:
            try:
                parsed_date = self._parse_date(date_str)
                return parsed_date.strftime("%Y%m%d")
            except Exception:
                continue

        return None

    def _parse_date(self, line: str) -> Any:
        """Parse date string to datetime object."""
        line = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', line)
        if '.' in line:
            return parser.parse(line, dayfirst=True)
        elif '/' in line:
            return parser.parse(line, dayfirst=False)
        else:
            return parser.parse(line, dayfirst=True)


    def extract_invoice_id(self, lines: List[str]) -> Optional[str]:
        """Extract invoice ID from lines."""
        invoice_triggers = self.config.get("metadata_triggers", {}).get("invoice_id", [])

        for line in lines:
            for trigger in invoice_triggers:
                if trigger in line:
                    invoice_number = (
                        line.replace(trigger, "")
                            .replace(":", "")
                            .replace(". ", "")
                            .replace(")", "")
                            .strip()
                    )
                    invoice_number = invoice_number.split(" ")[0]
                    return invoice_number
        return None