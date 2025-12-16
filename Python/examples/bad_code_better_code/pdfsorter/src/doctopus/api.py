import glob
import os
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from .config import _load_doctopus_config
from .models import _ProcessingContext
from .extractors.text import _TextProcessor
from .extractors.metadata import _MetadataExtractor
from .extractors.special_cases import _SpecialCaseHandler
from .classifier import classify_document
from .filer import _FileMover
from .shuttle import shuttle_service

from ..utils.logging import log_and_display, get_configured_logger, trackerator
from ..events.bus import publish_file_moved, publish_file_deleted

logger = get_configured_logger("DoctopusPrime")


class DoctopusPrime:
    """Single PDF processor with configurable classification and filing."""

    def __init__(
        self,
        pdf_filepath: str,
        base_dir: Optional[str] = None,
        config_path: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        dry_run: bool = False
    ):
        self.pdf_filepath = pdf_filepath
        self.dry_run = dry_run

        # Configuration
        self.config = _load_doctopus_config(config_path, config)

        # Base directory
        if base_dir:
            self.base_dir = base_dir
        elif "target_dir" in self.config:
            self.base_dir = self.config["target_dir"]
        else:
            self.base_dir = str(Path.home() / "BryBoxPDFs")

        # Sub-processors
        self.text_processor = _TextProcessor(self.config)
        self.metadata_extractor = _MetadataExtractor(self.config)
        self.special_handler = _SpecialCaseHandler()
        self.file_mover = _FileMover(self.base_dir, dry_run)

    # ------------------------------------------------------------------
    # Core pipeline
    # ------------------------------------------------------------------
    def process(self) -> _ProcessingContext:
        """
        Process the PDF file through the complete pipeline.

        Returns:
            _ProcessingContext with all extracted information
        """
        ctx = _ProcessingContext(
            pdf_filepath=self.pdf_filepath,
            base_dir=self.base_dir
        )

        # Extract text
        ctx.content = self.text_processor.extract_content(self.pdf_filepath)

        # Classify
        ctx.category = classify_document(ctx.content, self.config)

        # Relevant lines
        ctx.condensed_lines = self.text_processor.reduce_to_relevant_lines(ctx.content)

        # Special cases
        if ctx.category:
            ctx.condensed_lines = self.special_handler.handle_special_cases(
                ctx.category, ctx.condensed_lines
            )

        # Metadata
        ctx.document_date = self.metadata_extractor.extract_date(ctx.condensed_lines)
        ctx.invoice_id = self.metadata_extractor.extract_invoice_id(ctx.condensed_lines)

        # Build filename
        filename_stem = self._get_filename_component(ctx.category or "")
        ctx.output_filename = self._build_filename(
            ctx.document_date, filename_stem, ctx.invoice_id
        )

        # Build paths
        if ctx.category:
            built_path = self.file_mover.build_output_path(
                ctx.category, ctx.output_filename, self.config, self.pdf_filepath
            )
            ctx.output_filepath = built_path or ""
            ctx.backup_path = self.file_mover.get_backup_path(ctx.output_filepath)

        return ctx

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_filename_component(self, category: str) -> str:
        """Return the filename associated with the given category."""
        categories = self.config.get("categories", {})
        category_config = categories.get(category, {})
        return category_config.get("filename", category)

    def _build_filename(
        self,
        date: Optional[str],
        category: Optional[str],
        invoice_id: Optional[str]
    ) -> str:
        """Build output filename from components."""
        parts = []
        if date:
            parts.append(date)
        if category:
            parts.append(category)
        if invoice_id:
            parts.append(invoice_id)
        filename = " ".join(parts).strip()
        return f"{filename}.pdf"

    # ------------------------------------------------------------------
    # Public action
    # ------------------------------------------------------------------
    def shuttle_service(self, include_backup: bool = False) -> bool:
        """
        Move file to organised location.

        Args:
            include_backup: Whether to create backup copy

        Returns:
            True if file was successfully processed
        """
        ctx = self.process()
        return shuttle_service(
            ctx, self.file_mover, include_backup=include_backup, dry_run=self.dry_run
        )

    # ------------------------------------------------------------------
    # Convenience properties (no side effects)
    # ------------------------------------------------------------------
    @property
    def category(self) -> Optional[str]:
        ctx = self.process()
        return ctx.category

    @property
    def document_date(self) -> Optional[str]:
        ctx = self.process()
        return ctx.document_date

    @property
    def invoice_id(self) -> Optional[str]:
        ctx = self.process()
        return ctx.invoice_id


class DoctopusPrimeNexus:
    """Batch PDF processor with shared configuration."""

    def __init__(
        self,
        dir_path: str,
        base_dir: Optional[str] = None,
        config_path: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        processor_class: Type[DoctopusPrime] = DoctopusPrime
    ):
        self.dir_path = dir_path
        self.base_dir = base_dir
        self.dry_run = dry_run
        self.processor_class = processor_class
        self.config = _load_doctopus_config(config_path, config)

    def process_all(
        self,
        include_backup: bool = False,
        progress_bar: bool = True,
    ) -> Dict[str, bool]:
        """
        Process all PDF files in directory.

        Args:
            include_backup: Whether to create backup copies
            progress_bar: Whether to show progress bar

        Returns:
            Dict mapping file paths to success status
        """
        pdf_files = glob.glob(os.path.join(self.dir_path, "*.pdf"))
        results = {}

        log_and_display(
            f"Processing {len(pdf_files)} PDF file(s) in {self.dir_path}",
            sticky=True
        )
        pdf_files = (
            trackerator(
                pdf_files,
                description="Processing PDFs",
                final_message="All PDFs processed!"
            )
            if progress_bar
            else pdf_files
        )

        for pdf_file in pdf_files:
            try:
                processor = self.processor_class(
                    pdf_filepath=pdf_file,
                    base_dir=self.base_dir,
                    config=self.config,
                    dry_run=self.dry_run
                )
                success = processor.shuttle_service(include_backup=include_backup)
                results[pdf_file] = success
            except Exception as e:
                msg = f"Error processing {pdf_file}: {e}"
                if progress_bar:
                    log_and_display(msg)
                else:
                    log_and_display(msg)
                results[pdf_file] = False

        return results
    



    