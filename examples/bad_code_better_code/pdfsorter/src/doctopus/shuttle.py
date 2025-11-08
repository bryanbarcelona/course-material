from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import _ProcessingContext
    from .filer import _FileMover

def shuttle_service(
    ctx: "_ProcessingContext",
    file_mover: "_FileMover",
    include_backup: bool = False,
    dry_run: bool = False
) -> bool:
    """
    Move file to organised location and optionally back it up.
    Returns True if the whole pipeline succeeded.
    """
    if not ctx.category or not ctx.output_filepath:
        return False

    # Move main file
    success, is_new = file_mover.move_file(ctx.pdf_filepath, ctx.output_filepath)
    if not success:
        return False

    ctx.is_new_file = is_new

    # Create backup if requested
    if include_backup and ctx.backup_path and not dry_run:
        file_mover.backup_file(ctx.output_filepath, ctx.backup_path)

    return True