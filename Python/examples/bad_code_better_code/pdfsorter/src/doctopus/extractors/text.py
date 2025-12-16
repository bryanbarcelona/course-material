"""
PDF text extraction + line filtering.
"""

import re
from typing import List, Dict, Any
import pdfplumber

class _TextProcessor:
    """Handles PDF text extraction and line filtering."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------
    def extract_content(self, pdf_path: str) -> str:
        """Extract text content from PDF."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                page = pdf.pages[0]
                text = page.extract_text()
            return text or ""
        except Exception:
            return ""

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------
    def reduce_to_relevant_lines(self, content: str) -> List[str]:
        """Filter content to relevant lines based on extraction rules."""
        extraction_rules = self.config.get("extraction_rules", {})

        months = [
            "January", "Januar", "February", "Februar", "March", "März", "April",
            "May", "Mai", "June", "Juni", "July", "Juli", "August", "September",
            "October", "Oktober", "November", "December", "Dezember"
        ]

        month_translations = {
            "January": "Januar", "February": "Februar", "March": "März", "May": "Mai",
            "June": "Juni", "July": "Juli", "October": "Oktober", "Oct": "Okt",
            "December": "Dezember", "Dec": "Dez"
        }

        relevant_lines = []
        lines = content.split("\n")

        # Replace translated months
        for i, line in enumerate(lines):
            for key, value in month_translations.items():
                if key not in line:
                    lines[i] = lines[i].replace(value, key)

        for i, line in enumerate(lines):
            # Keep lines that contain any month name
            if any(substring in line for substring in month_translations.keys() | month_translations.values()):
                relevant_lines.append(line)

            # Extraction-rule triggers
            for trigger_type, triggers in extraction_rules.items():
                for trigger in triggers:
                    if trigger in line:
                        if trigger_type == "same_line":
                            line = f"{trigger}{line.split(trigger)[-1]}"
                            relevant_lines.append(line.replace(trigger, "").replace(":", "").strip())
                            relevant_lines.append(line)
                        elif trigger_type == "previous_line" and i > 0:
                            relevant_lines.append(lines[i - 1])
                        elif trigger_type == "next_line" and i < len(lines) - 1:
                            relevant_lines.append(lines[i + 1])

            if any(month.lower() in line.lower() for month in months):
                relevant_lines.append(line)

        return relevant_lines if relevant_lines else lines