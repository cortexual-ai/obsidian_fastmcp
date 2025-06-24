from datetime import datetime
import logging
from models.note_models import ObsidianNote
from config.settings import get_vault_path
from utils.utils import get_file_creation_time

logger = logging.getLogger(__name__)


async def update_note(note: ObsidianNote):
    """
    Update an existing Obsidian note in the vault.

    Args:
        note (ObsidianNote): The note object containing updated information

    Returns:
        dict: A dictionary containing the update status and note information

    Raises:
        Exception: If the note cannot be found or updated
    """
    try:
        logger.info(f"Starting note update for title: {note.title}")
        vault_path = get_vault_path()

        # Construct the file path
        if note.folder:
            file_path = vault_path / note.folder / f"{note.title}.md"
        else:
            file_path = vault_path / f"{note.title}.md"

        logger.info(f"Target file path: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"Note not found: {file_path}")

        # Get creation date using utility function
        created_date = get_file_creation_time(str(file_path))

        # Format the note content with metadata
        formatted_content = f"""---
title: {note.title}
created: {created_date}
modified: {datetime.now().isoformat()}
tags: {", ".join(note.tags)}
aliases: {", ".join(note.aliases)}
related: {", ".join(note.related)}
category: {note.category}
type: {note.type}
summary: {note.summary}
---

{note.content}
"""

        # Write the updated content to file
        logger.info(f"Writing updated content to file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_content)

        logger.info(f"Note updated successfully at: {file_path}")

        return {
            "message": "Note updated successfully",
            "path": str(file_path),
            "title": note.title,
        }

    except Exception as e:
        logger.error(f"Error updating note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to update note: {str(e)}")
