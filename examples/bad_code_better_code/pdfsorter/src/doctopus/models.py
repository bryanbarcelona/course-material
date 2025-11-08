from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class _ProcessingContext:
    pdf_filepath: str
    base_dir: str
    content: str = ""
    category: Optional[str] = None
    condensed_lines: List[str] = field(default_factory=list)
    document_date: Optional[str] = None
    invoice_id: Optional[str] = None
    output_filename: str = ""
    output_filepath: str = ""
    backup_path: Optional[str] = None
    is_new_file: bool = True