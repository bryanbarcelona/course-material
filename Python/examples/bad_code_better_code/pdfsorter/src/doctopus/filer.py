"""
File movement, backup, and name-clash resolution.
"""

import glob
import os
import shutil
from pathlib import Path
from string import ascii_uppercase
from typing import Optional, Tuple

import pdfplumber
from ..utils.health_check import is_healthy
from ..utils.logging import log_and_display
from ..events.bus import publish_file_moved, publish_file_deleted

class _FileMover:
    """Handles file operations and path management."""

    def __init__(self, base_dir: str, dry_run: bool = False):
        self.base_dir = base_dir
        self.dry_run = dry_run

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------
    def get_backup_path(self, output_filepath: str) -> Optional[str]:
        """Generate backup path if backup drive exists."""
        for drive in ascii_uppercase:
            if os.path.exists(f"{drive}:\\log.backup"):
                if output_filepath:
                    backup_path = f"{drive}:{output_filepath.split(':')[1]}"
                    return backup_path
                break
        return None

    def build_output_path(
        self,
        category: str,
        filename: str,
        config: dict,
        pdf_filepath: str
    ) -> Optional[str]:
        """Build the complete output file path."""
        categories = config.get("categories", {})
        if category not in categories:
            return None

        relative_path = categories[category].get("output_path", "")
        filepath = os.path.join(self.base_dir, relative_path, filename).replace("/", "\\")

        if not os.path.isfile(filepath):
            return filepath

        # Check if files have same content
        try:
            if self._files_have_same_content(pdf_filepath, filepath):
                return filepath
        except Exception:
            pass

        # Handle filename conflicts
        return self._resolve_filename_conflict(filepath)

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------
    def _files_have_same_content(self, file1: str, file2: str) -> bool:
        """Check if two PDF files have the same content."""
        try:
            with pdfplumber.open(file1) as pdf1, pdfplumber.open(file2) as pdf2:
                content1 = pdf1.pages[0].extract_text() if pdf1.pages else ""
                content2 = pdf2.pages[0].extract_text() if pdf2.pages else ""
                return content1 == content2
        except Exception:
            return False

    def _resolve_filename_conflict(self, filepath: str) -> str:
        """Resolve filename conflicts by adding number suffix."""
        i = 1
        base, ext = os.path.splitext(filepath)
        while os.path.isfile(f"{base}({i}){ext}"):
            i += 1
        return f"{base}({i}){ext}"

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------
    def move_file(self, source: str, destination: str) -> Tuple[bool, bool]:
        """Move file from source to destination. Returns (success, is_new_file)."""
        if not os.path.exists(source):
            log_and_display(f"Source file does not exist: {source}")
            return False, False

        file_size = os.path.getsize(source)
        output_dir = os.path.dirname(destination)

        if self.dry_run:
            log_and_display(f"Would create directory: {output_dir}")
            if os.path.exists(destination):
                log_and_display(f"Would delete source file: {source}")
                return True, False
            else:
                log_and_display(f"Would move {source} to {destination}")
                return True, True

        # Create directory if needed
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Handle existing destination
        if os.path.exists(destination) and is_healthy(destination):
            os.remove(source)
            log_and_display(f"Destination exists. Deleted source file: {source}")
            publish_file_deleted(source, file_size)
            return True, False
        else:
            shutil.move(source, destination)
            if not is_healthy(destination):
                log_and_display(f"Moved file is corrupted: {destination}", level="error")
                return False, False

            log_and_display(f"Moved {source} to {destination}.")
            publish_file_moved(source, destination, file_size, True)
            return True, True

    def backup_file(self, source: str, backup_path: str) -> bool:
        """Create backup copy of file."""
        if not backup_path or not os.path.exists(source):
            return False

        if self.dry_run:
            log_and_display(f"Would backup {source} to {backup_path}")
            return True

        try:
            backup_dir = os.path.dirname(backup_path)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            shutil.copy(source, backup_path)
            log_and_display(f"Backed up {source} to {backup_path}.")
            return True
        except Exception as e:
            from ..utils.logging import logger
            logger.error(f"Failed to backup {source}: {e}")
            return False