"""
Category-specific post-processing.
"""

import re
from typing import List

class _SpecialCaseHandler:
    """Handles special-case processing for specific categories."""

    def handle_special_cases(self, category: str, lines: List[str]) -> List[str]:
        """Apply special-case handling based on category."""
        if category == "McDonalds Rechnung":
            return self._handle_mcdonalds(lines)
        return lines

    def _handle_mcdonalds(self, lines: List[str]) -> List[str]:
        """Handle McDonald's specific date format."""
        date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}\b'
        for i, line in enumerate(lines):
            match = re.search(date_pattern, line)
            if match:
                lines[i] = match.group(0).replace("/", ".")
        return lines